from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('commandes', '0001_initial'),  # Dépendance avec la migration initiale
    ]

    operations = [
        migrations.AddField(
            model_name='Commande',
            name='idClient',
            field=models.IntegerField(default=0),  # Valeur par défaut temporaire
        ),
    ]