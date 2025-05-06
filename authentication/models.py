from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('AGRI', 'Agriculteur'),
        ('ACHETEUR', 'Acheteur'),
        ('ADMIN', 'Administrateur'),
    )
    
    # Champs personnalisés
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES)
    
    # Résolution des conflits
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name="agrolink_user_set",
        related_query_name="agrolink_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="agrolink_user_set",
        related_query_name="agrolink_user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Utilisateur"
        db_table = 'custom_user'  # Nom de table différent

# ... (AgentProfile et ClientProfile restent inchangés)

class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Agent {self.nom}"

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    
    def __str__(self):
        return f"Client {self.nom}"
