from django.db import models
from registrar.models import Contributor

class Objective(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField()
    implementation = models.CharField(max_length=256)
    prerequisites = models.ManyToManyField('self')

class Achievement(models.Model):
    objective = models.ForeignKey(Objective)
    contributor = models.ForeignKey(Contributor)
    awarded = models.DateTimeField()
    support_url = models.URLField()
    support_text = models.TextField()
    
