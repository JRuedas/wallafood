from django.db import models

# Create your models here.
class Advert(models.Model):
    id_advert = models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=False)
    vendor = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=False)
    amount_available = models.IntegerField()
    allergens =  models.CharField(max_length=200, null=False)
    vote_average = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    status = models.CharField(max_length=20)
    photo_url = models.CharField(max_length=300, default='https://www.telemundo.com/sites/nbcutelemundo/files/images/promo/video_clip/2017/12/21/frutas-y-verduras.jpg')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)