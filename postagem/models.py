from django.db import models
from users.models import User

class Posts(models.Model):
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering: ['-date']
        
    def __str__(self):
        return str(self.owner)+'s post'