# Generated by Django 3.1.5 on 2022-04-17 06:24

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import user.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("defaultPicker", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "twitter",
                    models.CharField(
                        blank=True, default="", max_length=255, verbose_name="Twitter"
                    ),
                ),
                (
                    "fullName",
                    models.CharField(
                        blank=True, default="", max_length=255, verbose_name="Full Name"
                    ),
                ),
                (
                    "gender",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[(0, "Male"), (1, "Female"), (2, "Prefer not to say")],
                        null=True,
                    ),
                ),
                (
                    "about",
                    models.CharField(
                        blank=True, default="", max_length=255, verbose_name="Bio"
                    ),
                ),
                ("location", models.CharField(blank=True, default="", max_length=255)),
                ("isOnline", models.BooleanField(default=False)),
                (
                    "familyPlans",
                    models.PositiveBigIntegerField(
                        blank=True,
                        choices=[
                            (0, "Don’t want kids"),
                            (1, "Want kids"),
                            (2, "Open to kids"),
                            (3, "Have kids"),
                            (4, "Prefer not to say"),
                            (5, "Je ne veux pas d'enfants"),
                            (6, "Je veux des enfants"),
                            (7, "Ouvert aux enfants"),
                            (8, "J'ai des enfants"),
                            (9, "Je préfère ne rien dire"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "politics",
                    models.PositiveBigIntegerField(
                        blank=True,
                        choices=[
                            (0, "Liberal"),
                            (1, "Liberal"),
                            (2, "Conservative"),
                            (3, "Other"),
                            (4, "Prefer Not to Say"),
                            (5, "Libéral"),
                            (6, "Modéré"),
                            (7, "Conservateur"),
                            (8, "Autre"),
                            (9, "Je préfère ne rien dire"),
                        ],
                        null=True,
                    ),
                ),
                ("gift_coins", models.PositiveIntegerField(default=0)),
                ("purchase_coins", models.PositiveIntegerField(default=0)),
                ("zodiacSign", models.PositiveBigIntegerField(blank=True, null=True)),
                (
                    "interestedIn",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "interested_in",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "ethinicity",
                    models.PositiveBigIntegerField(
                        blank=True,
                        choices=[
                            (0, "American Indian"),
                            (1, "Black/ African Descent"),
                            (2, "East Asian"),
                            (3, "Hispanic / Latino"),
                            (4, "Middle Eastern"),
                            (5, "Pacific Islander"),
                            (6, "South Asian"),
                            (7, "White / Caucasian"),
                            (8, "Other"),
                            (9, "Prefer Not to Say"),
                            (10, "Amérindien"),
                            (11, "Noir / Afro Descendant"),
                            (12, "Asie de L'Est"),
                            (13, "Hispanique / latino"),
                            (14, "Moyen-Orient"),
                            (15, "Insulaire du Pacifique"),
                            (16, "Sud-Asiatique"),
                            (17, "Blanc / Caucasien"),
                            (18, "Autre"),
                            (19, "Je préfère ne rien dire"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "religion",
                    models.PositiveBigIntegerField(
                        blank=True,
                        choices=[
                            (0, "Agnostic"),
                            (1, "Atheist"),
                            (2, "Buddhist"),
                            (3, "Catholic"),
                            (4, "Christian"),
                            (5, "Hindu"),
                            (6, "Jewish"),
                            (7, "Muslim"),
                            (8, "Spiritual"),
                            (9, "Other"),
                            (10, "Prefer Not to Say"),
                            (10, "Agnostique"),
                            (11, "Athée"),
                            (12, "Bouddhiste"),
                            (13, "Catholique"),
                            (14, "Chrétien"),
                            (15, "Hindou"),
                            (16, "Juif"),
                            (17, "Musulman"),
                            (18, "Spirituel"),
                            (19, "Autre"),
                            (20, "Je préfère ne rien dire"),
                        ],
                        null=True,
                    ),
                ),
                ("is_blocked", models.BooleanField(default=False)),
                ("education", models.CharField(blank=True, max_length=265, null=True)),
                ("work", models.CharField(blank=True, max_length=265, null=True)),
                ("photos_quota", models.SmallIntegerField(default=3)),
                ("avatar_index", models.IntegerField(default=0)),
                (
                    "onesignal_player_id",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "age",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="defaultPicker.age",
                        verbose_name="Age",
                    ),
                ),
                (
                    "blockedUsers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="blocked_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("book", models.ManyToManyField(blank=True, to="defaultPicker.book")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "height",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="defaultPicker.height",
                        verbose_name="Height",
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_user_likes_+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "movies",
                    models.ManyToManyField(blank=True, to="defaultPicker.movies"),
                ),
                ("music", models.ManyToManyField(blank=True, to="defaultPicker.music")),
                (
                    "owned_by",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="fake_users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CoinSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("method", models.CharField(max_length=70)),
                ("coins_needed", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="UserRole",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("REGULAR", "REGULAR"),
                            ("CHATTER", "CHATTER"),
                            ("ADMIN", "ADMIN"),
                            ("SUPER_ADMIN", "SUPER_ADMIN"),
                        ],
                        default="REGULAR",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkerInvitation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("token", models.UUIDField()),
                ("is_admin_permission", models.BooleanField()),
                ("is_chat_admin_permission", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="UserSocialProfile",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "platform",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "GOOGLE"),
                            (2, "FACEBOOK"),
                            (3, "INSTAGRAM"),
                            (4, "SNAPCHAT"),
                            (5, "LINKEDIN"),
                            (6, "REDDIT"),
                        ],
                        default=4,
                    ),
                ),
                ("url", models.URLField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Social Profile",
                "verbose_name_plural": "User Social Profiles",
            },
        ),
        migrations.CreateModel(
            name="UserPhoto",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        blank=True, null=True, upload_to=user.models.content_file_name
                    ),
                ),
                ("file_url", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avatar_photos",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CoinsHistory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("purchase_coins", models.IntegerField()),
                ("gift_coins", models.IntegerField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "actor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="coin_editor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coin_holder",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="roles",
            field=models.ManyToManyField(
                blank=True, related_name="users", to="user.UserRole"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="sportsTeams",
            field=models.ManyToManyField(blank=True, to="defaultPicker.sportsTeams"),
        ),
        migrations.AddField(
            model_name="user",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="profile_tags", to="defaultPicker.tags"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="tvShows",
            field=models.ManyToManyField(blank=True, to="defaultPicker.tvShows"),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
    ]
