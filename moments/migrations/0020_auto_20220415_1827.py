# Generated by Django 3.1.5 on 2022-04-15 12:42

from django.db import migrations, models
import django.db.models.deletion
import moments.models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("moments", "0019_genericcomment_genericlike"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genericcomment",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="genericlike",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="story",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to=moments.models.Story.get_avatar_path
            ),
        ),
    ]
