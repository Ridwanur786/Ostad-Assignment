from django.db import models

# Create your models here.

class Report(models.Model):
   REPORT_TYPES= [
      ('Lost',   'Lost'),
      ('Found', 'Found'),
   ]
   STATUS_CHOICES =[
      ('Active',  'Active'),
      ('Resolved',  'Resolved')
   ]

   item_name =models.CharField(max_length=200)
   type =models.CharField(max_length=10, choices=REPORT_TYPES)
   category=models.CharField(max_length=200)
   description=models.TextField()
   location=models.CharField(max_length=200)
   date=models.DateField()
   contact_info=models.CharField(max_length=200)
   image=models.ImageField(upload_to='report_image/', blank=True, null=True)
   status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active') 
   created_at=models.DateTimeField(auto_now_add=True)


   def __str__(self):
      return f"{self.item_name} ({self.type})"
   