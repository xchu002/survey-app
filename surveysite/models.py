from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Survey(models.Model):
    unique_id = models.CharField(max_length=6, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    survey_question = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiry_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ('unique_id',)

    def __str__(self):
        return f"id: {self.unique_id}, {self.user}, {self.survey_question}"

class Response(models.Model):
    question = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True, related_name="answers")
    answer = models.TextField(null=True)

    def __str__(self):
        return f"{self.question}, {self.answer}"