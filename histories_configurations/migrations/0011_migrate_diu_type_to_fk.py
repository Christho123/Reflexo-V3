# Generated manually to migrate diu_type data to ForeignKey

from django.db import migrations

def migrate_diu_type_data(apps, schema_editor):
    """Migrate existing diu_type_id values to DIUType records"""
    DIUType = apps.get_model('histories_configurations', 'DIUType')
    History = apps.get_model('histories_configurations', 'History')
    
    # Get all unique diu_type_id values from the database
    cursor = schema_editor.connection.cursor()
    cursor.execute("SELECT DISTINCT diu_type_id FROM histories WHERE diu_type_id IS NOT NULL AND diu_type_id != ''")
    unique_values = [row[0] for row in cursor.fetchall()]
    
    # Create DIUType records for each unique value
    diu_type_mapping = {}
    for value in unique_values:
        diu_type, created = DIUType.objects.get_or_create(name=value)
        diu_type_mapping[value] = diu_type.id
        if created:
            print(f"Created DIUType: {value} (ID: {diu_type.id})")
        else:
            print(f"Found existing DIUType: {value} (ID: {diu_type.id})")
    
    # Update histories records to use the new IDs
    for old_value in unique_values:
        if old_value in diu_type_mapping:
            # Update the diu_type_id field to point to the new DIUType
            cursor.execute(
                "UPDATE histories SET diu_type_id = %s WHERE diu_type_id = %s",
                [diu_type_mapping[old_value], old_value]
            )
            affected_rows = cursor.rowcount
            print(f"Updated {affected_rows} histories: '{old_value}' -> {diu_type_mapping[old_value]}")

def reverse_migrate_diu_type_data(apps, schema_editor):
    """Reverse migration - convert back to string values"""
    DIUType = apps.get_model('histories_configurations', 'DIUType')
    
    # Convert back to string values
    cursor = schema_editor.connection.cursor()
    cursor.execute("SELECT id, diu_type_id FROM histories WHERE diu_type_id IS NOT NULL")
    histories = cursor.fetchall()
    
    for history_id, diu_type_id in histories:
        if isinstance(diu_type_id, int):
            try:
                diu_type = DIUType.objects.get(id=diu_type_id)
                cursor.execute(
                    "UPDATE histories SET diu_type_id = %s WHERE id = %s",
                    [diu_type.name, history_id]
                )
                print(f"Reverted history {history_id}: {diu_type_id} -> '{diu_type.name}'")
            except DIUType.DoesNotExist:
                print(f"DIUType with ID {diu_type_id} not found for history {history_id}")

class Migration(migrations.Migration):

    dependencies = [
        ('histories_configurations', '0010_diutype'),
    ]

    operations = [
        migrations.RunPython(
            migrate_diu_type_data,
            reverse_migrate_diu_type_data,
        ),
    ]
