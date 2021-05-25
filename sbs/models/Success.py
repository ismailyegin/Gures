from django.db import models



class Success(models.Model):


    Olimpiyat = 'Olimpiyat'
    Dunya = 'Dunya'
    Avrupa = 'Avrupa'


    type = (
        (Olimpiyat, 'Olimpiyat'),
        (Dunya, 'Dunya'),
        (Avrupa, 'Avrupa'),
    )
    type = models.CharField(max_length=128, verbose_name='Madalya', choices=type, default=Dunya)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()



