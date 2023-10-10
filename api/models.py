from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator
import datetime, ast
from django.contrib.auth.models import User, Group
from django.utils import timezone
DIABETES_TYPES = [
    ("Type 1", "Type 1"),
    ("Type 2", "Type 2"),
]

SEX_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
]
# Create your models here.
class Users(User):
    #Included fields in the User class
    # First name 
    # Last name 
    # Email 
    # Password 
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        default=2.50,
        verbose_name="User Weight",
        validators=[
            MinValueValidator(2.00, message="Weight cannot be lower than 2.5 Kg"),
            MaxValueValidator(650.00, message="Weight cannot be more than 650 KG"),
    ],
)

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        default=45.00,
        verbose_name="User Height",
        validators=[
        MinValueValidator(45.00, message="Height cannot be less than 45cm"),
        MaxValueValidator(280.00, message="Height cannot be taller than 280 cm tall"),
    ],
)

    diabetes_type = models.CharField(
        max_length=6,
        choices=DIABETES_TYPES,
        default='Type 1',  
        verbose_name="Diabetes Type"
    )

    sex = models.CharField(
        max_length= 6,
        choices= SEX_CHOICES,
        default="male",
        verbose_name= "User Sex"
    )

    class Meta:
        verbose_name_plural = "Users"
        ordering = ['id']

    def getUserInformation(self):
        return f"{self.first_name} {self.last_name} {self.sex} {self.diabetes_type}"
    
    
    def __str__(self):
        return self.getUserInformation()
    
    def generate_username(self):
        # Combine first_name and last_name, and make it lowercase
        username = f"{self.first_name.lower()}{self.last_name.lower()}"
        x = username.strip(' ')
        return x

    def save(self, *args, **kwargs):
        if not self.username:
            # Generate the username if it's empty
            self.username = self.generate_username()
            
        super().save(*args, **kwargs)


class GlucoseReading(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    blood_sugar_level = models.DecimalField(max_digits=5, decimal_places=1)

    class Meta: 
        verbose_name_plural = "User Glucose Readings"
    
    def __str__(self):
        return f"{self.date} {self.time} {self.blood_sugar_level}"