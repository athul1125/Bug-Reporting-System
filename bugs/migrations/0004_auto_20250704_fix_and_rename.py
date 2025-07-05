from django.db import migrations, models
import django.db.models.deletion

def convert_fixed_by_to_foreign_key(apps, schema_editor):
    Bug = apps.get_model('bugs', 'Bug')
    User = apps.get_model('auth', 'User')
    
    # Clear any invalid data first
    Bug.objects.filter(fixed_by__startswith='User').update(fixed_by=None)
    
    # For each bug with valid fixed_by username
    for bug in Bug.objects.exclude(fixed_by='').exclude(fixed_by__isnull=True):
        try:
            # Try to find user by username
            user = User.objects.filter(username=bug.fixed_by).first()
            if user:
                bug.fixed_by_new = user
                bug.save()
        except Exception:
            # If any error occurs, set to None
            bug.fixed_by_new = None
            bug.save()

class Migration(migrations.Migration):
    dependencies = [
        ('bugs', '0003_alter_bug_fixed_by'),
    ]

    operations = [
        # First rename status_updated_by to updated_by
        migrations.RenameField(
            model_name='bug',
            old_name='status_updated_by',
            new_name='updated_by',
        ),
        
        # Add new fixed_by field temporarily
        migrations.AddField(
            model_name='bug',
            name='fixed_by_new',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='bug_fixer',
                to='auth.user'
            ),
        ),
        
        # Run the data migration
        migrations.RunPython(convert_fixed_by_to_foreign_key),
        
        # Remove old fixed_by field
        migrations.RemoveField(
            model_name='bug',
            name='fixed_by',
        ),
        
        # Rename new field to fixed_by
        migrations.RenameField(
            model_name='bug',
            old_name='fixed_by_new',
            new_name='fixed_by',
        ),
    ]
