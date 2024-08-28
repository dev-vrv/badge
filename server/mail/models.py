from django.db import models

# Create your models here.
class Mails(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sender = models.EmailField()
    recipient = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
