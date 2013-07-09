from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
	def create_user(self, email, date_of_birth, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=MyUserManager.normalize_email(email),
			date_of_birth=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, date_of_birth, password):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(email,
			password=password,
			date_of_birth=date_of_birth
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


class MyUser(AbstractBaseUser):
	name = models.CharField(max_length=40)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
		db_index=True,
	)
	date_of_birth = models.DateField()
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['date_of_birth']

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def __unicode__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

class Blog(models.Model):
	owner = models.ForeignKey(MyUser, unique = True)

class Post(models.Model):
	blog = models.ForeignKey(Blog)
	title = models.CharField(max_length='1000')
	description = models.CharField(max_length = "5000")
	date = models.DateTimeField()
	

class Comment(models.Model):
	content = models.CharField(max_length = "200")
	post = models.ForeignKey(Post)
	commentor = models.ForeignKey(MyUser)
	date = models.DateTimeField()