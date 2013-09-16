from django.db import models


class WaterTankController(models.Model):

    pumpIsOn        = models.BooleanField('Pump On', default=False)
    alarmLow        = models.BooleanField('Alarm Low Activated', default=False)
    alarmHighActive = models.BooleanField('Alarm High Activated', default=False)

    autoOn          = models.BooleanField('Auto On', default=False)
    autoOff         = models.BooleanField('Auto Off', default=False)
 

    def __unicode__(self):  # Python 3: def __str__(self):
        return 'Water Tank controller'


# Create your models here.
