from django.db import models

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

class Similar(models.Model):
    id = models.IntegerField(primary_key=True)
    correct_cat_name = models.TextField()
    similar_cat_name = models.TextField()
    npy_id = models.IntegerField()

    def __str__(self):
        return ''.format([self.correct_cat_name, self.similar_cat_name, self.npy_id])