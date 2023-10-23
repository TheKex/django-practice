from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=400, blank=True, default='')

    def __str__(self):
        return f"Sensor '{self.name}': {self.description}"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sensor}, temp - {self.temperature}, {self.create_at}'
