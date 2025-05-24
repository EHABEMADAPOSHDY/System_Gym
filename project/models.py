from django.db import models
import datetime
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def get_default_training():
    training, created = Training_name.objects.get_or_create(name='Toning')
    return training.id

# التحقق من أن رقم الهاتف يتكون من 11 رقم ويبدأ بـ 01
phone_validator = RegexValidator(
    regex=r'^01\d{9}$',
    message="رقم الهاتف يجب أن يبدأ بـ 01 ويتكون من 11 رقمًا."
)

class Training_name(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    name = models.CharField(max_length=50, verbose_name='الاسم')

    mobil1 = models.CharField(
        max_length=11,
        verbose_name='رقم التليفون 1',
        validators=[phone_validator]
    )
    mobil2 = models.CharField(
        max_length=11,
        verbose_name='رقم التليفون 2',
        validators=[phone_validator]
    )

    Length_umber = models.CharField(max_length=12, verbose_name='رقم الطوارئ', null=True, blank=True)
    National_ID = models.CharField(max_length=25, verbose_name='الرقم القومي', null=True, blank=True)
    the_address = models.TextField(max_length=200, verbose_name='العنوان')
    the_rest = models.IntegerField(verbose_name='باقي', null=True, blank=True)

    Type_of_training = models.ForeignKey(
        Training_name,
        on_delete=models.PROTECT,
        verbose_name='نوع التدريب',
        default=get_default_training
    )

    Number_of_sessions = models.IntegerField(verbose_name='عدد الجلسات', max_length=4)
    Start_date = models.DateField(verbose_name='تاريخ البداية', default=datetime.date.today, null=True, blank=True)
    Daytime_date = models.DateField(verbose_name='تاريخ النهاية', null=True, blank=True)

    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='باركود')
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True, verbose_name='صورة الباركود')

    def __str__(self):
        return self.name

    def clean(self):
        if Subscriber.objects.exclude(pk=self.pk).filter(name=self.name).exists():
            raise ValidationError({'name': 'هذا الاسم مسجل بالفعل.'})

        if Subscriber.objects.exclude(pk=self.pk).filter(mobil1=self.mobil1).exists():
            raise ValidationError({'mobil1': 'رقم الهاتف هذا مسجل بالفعل.'})

    def save(self, *args, **kwargs):
        if self.Start_date and not self.Daytime_date:
            self.Daytime_date = self.Start_date + relativedelta(months=1)

        self.full_clean()
        super().save(*args, **kwargs)

        if not self.barcode:
            name_part = self.name.upper().replace(" ", "")[:5] if self.name else "USER"
            self.barcode = f"SUB-{self.id}-{name_part}"
            super().save(update_fields=['barcode'])

        if not self.barcode_image:
            barcode_buffer = BytesIO()
            barcode_value = f"SUB-{self.id}"
            writer_options = {
                'write_text': False,
                'module_height': 10.0,
                'module_width': 0.3,
                'quiet_zone': 0.0,
            }

            Code128(barcode_value, writer=ImageWriter()).write(barcode_buffer, options=writer_options)

            barcode_buffer.seek(0)
            image = Image.open(barcode_buffer).convert('RGB')
            image.save(barcode_buffer, format='PNG', dpi=(300, 300))

            filename = f"barcode_{self.id}.png"
            self.barcode_image.save(filename, ContentFile(barcode_buffer.getvalue()), save=True)
