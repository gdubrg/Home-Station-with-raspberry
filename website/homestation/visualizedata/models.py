from django.db import models


# class HandleSettings():
#
#     def __init__(self):
#         self.temperature = 0
#         self.temperature += 1
#
#     def get_temperature(self):
#         return self.temperature
#

# Create your models here.

class Sensor(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    name = models.CharField(max_length=30, help_text='Enter sensors name')
    description = models.CharField(max_length=255, help_text='Enter sensors description')

    # Metadata
    class Meta:
        ordering = ['name']

    # Methods
    # def get_absolute_url(self):
    #     """Returns the url to access a particular instance of MyModelName."""
    #     return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name


class Values(models.Model):

    sensor = models.ForeignKey(Sensor, related_name='values', on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    timestamp = models.DateTimeField()