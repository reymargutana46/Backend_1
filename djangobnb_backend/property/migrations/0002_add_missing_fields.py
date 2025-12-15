# Clean migration - no operations needed since category already exists in 0001_initial
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
    ]
