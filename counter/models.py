from math import sqrt

from django.db import models


class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()

    #calculate distance beetween two points accroding to the formula
    def calculate_distance(self, point):
        return sqrt(pow(self.x - point.x, 2) + pow(self.y - point.y, 2))
