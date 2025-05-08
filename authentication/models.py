from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('AGRI', 'Agriculteur'),
        ('ACHETEUR', 'Acheteur'),
        ('ADMIN', 'Administrateur'),
    )
    
    # Personal Information
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    
    # Roles and Permissions
    role = models.CharField(max_length=10, choices=ROLES, default='ACHETEUR')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    # Groups and Permissions with custom related names
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="agrolink_user_set",
        related_query_name="agrolink_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="agrolink_user_set",
        related_query_name="agrolink_user",
    )

    # Authentication fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'custom_user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class AgentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='agent_profile',
        limit_choices_to={'role': 'AGRI'}
    )
    nom = models.CharField(_('nom complet'), max_length=100)
    region = models.CharField(_('région'), max_length=100)
    phone = models.CharField(_('téléphone'), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('Profil Agriculteur')
        verbose_name_plural = _('Profils Agriculteurs')
    
    def __str__(self):
        return f"Agriculteur {self.nom} ({self.region})"


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile',
        limit_choices_to={'role': 'ACHETEUR'}
    )
    nom = models.CharField(_('nom complet'), max_length=100)
    adresse = models.TextField(_('adresse complète'))
    company = models.CharField(_('entreprise'), max_length=100, blank=True)
    phone = models.CharField(_('téléphone'), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('Profil Acheteur')
        verbose_name_plural = _('Profils Acheteurs')
    
    def __str__(self):
        return f"Acheteur {self.nom}" + (f" ({self.company})" if self.company else "")