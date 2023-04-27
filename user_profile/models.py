# import uuid
from accounts.models import User
from django.db import models

# Create your models here.
class OwnerProfile(models.Model):
	
	# id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
	first_name = models.CharField(max_length=50, unique=False)
	last_name = models.CharField(max_length=50, unique=False)
	phone_number = models.CharField(max_length=10, unique=True)
	# age = models.PositiveIntegerField(null=False, blank=False)
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
	class Meta:
		db_table = "owner_profile"

	def __str__(self) -> str:
		return self.first_name