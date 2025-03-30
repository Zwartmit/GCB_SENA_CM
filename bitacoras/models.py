from django.db import models
from django.conf import settings
import os
import uuid

def bitacora_file_path(instance, filename):
    """Generate file path for new bitacora file"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/bitacoras/', filename)

class Bitacora(models.Model):
    apprentice = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bitacoras',
        limit_choices_to={'user_type': 'apprentice'}
    )
    file = models.FileField(upload_to=bitacora_file_path)
    filename = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Bitácora'
        verbose_name_plural = 'Bitácoras'
    
    def __str__(self):
        return f"Bitácora: {self.filename} by {self.apprentice.username}"
    
    def save(self, *args, **kwargs):
        if not self.filename and self.file:
            self.filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Delete file from filesystem when deleting the model instance"""
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
