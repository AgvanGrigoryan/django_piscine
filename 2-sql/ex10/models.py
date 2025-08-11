from django.db import models

class Planets(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    climate = models.CharField(max_length=255, null=True, blank=True)
    diameter = models.IntegerField(null=True, blank=True)
    orbital_period = models.IntegerField(null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    rotation_period = models.IntegerField(null=True, blank=True)
    surface_water = models.FloatField(null=True, blank=True)
    terrain = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    birth_year = models.CharField(max_length=32, null=True, blank=True)
    gender = models.CharField(max_length=32, null=True, blank=True)
    eye_color = models.CharField(max_length=32, null=True, blank=True)
    hair_color = models.CharField(max_length=32, null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    mass = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    homeworld = models.ForeignKey(Planets,
                                    db_column='homeworld',
                                    to_field='name',
                                    null=False,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Movies(models.Model):
    episode_nb = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64, unique=True, null=False)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(max_length=64, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)

    def __str__(self):
        return self.title
