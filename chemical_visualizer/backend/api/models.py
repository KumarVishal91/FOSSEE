from django.db import models


class Dataset(models.Model):

    name = models.CharField(max_length=200)

    file = models.FileField(upload_to='csv/')

    row_count = models.PositiveIntegerField(default=0)

    columns = models.JSONField(default=list)

    data = models.JSONField(default=list)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    summary = models.JSONField()

    def __str__(self):
        return self.name
