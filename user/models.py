import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.core.cache import cache
from django.db import connection, models
from django.utils.html import format_html
from django.utils import timezone

from defaultPicker.models import Language
from defaultPicker.models import age as Age
from defaultPicker.models import book as Book
from defaultPicker.models import height as Height
from defaultPicker.models import movies as Movies
from defaultPicker.models import music as Music
from defaultPicker.models import sportsTeams as SportsTeams
from defaultPicker.models import tags as Tags
from defaultPicker.models import tvShows as TvShows

from gifts.models import RealGift, VirtualGift, RealGiftPriceForRegion, VirtualGiftPriceForRegion
from purchase.models import CoinPrices, CoinPricesForRegion, Plan, PlanForRegion

from .middleware import RequestMiddleware

from push_notifications.models import GCMDevice
from defaultPicker.utils import language_translate, SUPPORTED_LANGUAGES
from django_countries import countries

ETHINICITY_TYPE = (
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
)

FAMILY_CHOICE = (
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
)

POLITICS_CHOICE = (
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
)

RELIGIOUS_CHOICE = (
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
)


class UserRole(models.Model):
    ROLE_REGULAR = "REGULAR"
    ROLE_CHATTER = "CHATTER"
    ROLE_ADMIN = "ADMIN"
    ROLE_SUPER_ADMIN = "SUPER_ADMIN"
    ROLE_FAKE_USER = "MODERATOR"

    ROLES = (
        (ROLE_REGULAR, ROLE_REGULAR),
        (ROLE_CHATTER, ROLE_CHATTER),
        (ROLE_ADMIN, ROLE_ADMIN),
        (ROLE_SUPER_ADMIN, ROLE_SUPER_ADMIN),
        (ROLE_FAKE_USER, ROLE_FAKE_USER),
    )
    role = models.CharField(choices=ROLES, max_length=20,
                            default="REGULAR", null=False)

    def __str__(self):
        return self.role


class User(AbstractUser):
    def get_avatar_path(self, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "static/uploads/images/avatar/" + filename

    INTEREST_CHOICES = (
        (1, "SERIOUS_RELATIONSHIP_ONLY_MALE"),
        (2, "SERIOUS_RELATIONSHIP_ONLY_FEMALE"),
        (3, "SERIOUS_RELATIONSHIP_BOTH"),
        (4, "CAUSAL_DATING_ONLY_MALE"),
        (5, "CAUSAL_DATING_ONLY_FEMALE"),
        (6, "CAUSAL_DATING_BOTH"),
        (7, "NEW_FRIENDS_ONLY_MALE"),
        (8, "NEW_FRIENDS_ONLY_FEMALE"),
        (9, "NEW_FRIENDS_BOTH"),
        (10, "ROOM_MATES_ONLY_MALE"),
        (11, "ROOM_MATES_ONLY_FEMALE"),
        (12, "ROOM_MATES_BOTH"),
        (13, "BUSINESS_CONTACTS_ONLY_MALE"),
        (14, "BUSINESS_CONTACTS_ONLY_FEMALE"),
        (15, "BUSINESS_CONTACTS_BOTH"),
    )
    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
        (3, "Prefer not to say"),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    email = models.EmailField(null=False, blank=False)
    twitter = models.CharField(
        max_length=255, default="", blank=True, verbose_name="Twitter"
    )
    # first_name = None
    # last_name = None
    fullName = models.CharField(
        max_length=255, default="", blank=True, verbose_name="Full Name"
    )
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, blank=True, null=True
    )
    about = models.CharField(max_length=255, default="",
                             blank=True, verbose_name="Bio")
    language = models.ManyToManyField(Language, blank=True)
    worker_id_code = models.IntegerField(default=0, editable=False)
    distance = models.CharField(
        max_length=255, default="", editable=False, blank=True, null=True
    )
    user_language_code = models.CharField(
        max_length=5, default="en", editable=False, blank=True, null=True
    )
    language_id_code = models.CharField(max_length=255, default="", blank=True)
    location = models.CharField(max_length=255, default="", blank=True)
    address = models.CharField(max_length=555, default="", blank=True)
    country = models.CharField(
        max_length=255, default=None, null=True, blank=True)
    country_code = models.CharField(
        max_length=50, default=None, null=True, blank=True)
    city = models.CharField(max_length=50, default=None, null=True, blank=True)
    state = models.CharField(
        max_length=50, default=None, null=True, blank=True)
    isOnline = models.BooleanField(default=False)

    familyPlans = models.PositiveBigIntegerField(
        choices=FAMILY_CHOICE, null=True, blank=True
    )
    # age = models.PositiveBigIntegerField(choices=AGE_RANGE, blank=True, null=True)
    tags = models.ManyToManyField(
        Tags, related_name="profile_tags", blank=True)
    politics = models.PositiveBigIntegerField(
        choices=POLITICS_CHOICE, blank=True, null=True
    )
    gift_coins = models.PositiveIntegerField(null=False, default=0)
    gift_coins_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True
    )  # last gift date
    purchase_coins = models.PositiveIntegerField(null=False, default=0)
    purchase_coins_date = models.DateTimeField(
        auto_now_add=False, null=True, blank=True
    )  # last purchase date
    zodiacSign = models.PositiveBigIntegerField(blank=True, null=True)
    # height = models.IntegerField(null=True, blank=True, default=0)
    # interestedIn = models.PositiveSmallIntegerField(choices=INTEREST_CHOICES, null=True, blank=True)
    interestedIn = models.CharField(max_length=256, blank=True, null=True)
    interested_in = models.CharField(max_length=256, blank=True, null=True)
    ethinicity = models.PositiveBigIntegerField(
        choices=ETHINICITY_TYPE, blank=True, null=True
    )
    religion = models.PositiveBigIntegerField(
        choices=RELIGIOUS_CHOICE, blank=True, null=True
    )

    # list of users this user has blocked, they can't message him now
    blockedUsers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="blocked_by"
    )

    # set this to true to block a user from using the app
    is_blocked = models.BooleanField(default=False)

    education = models.CharField(max_length=265, null=True, blank=True)

    music = models.ManyToManyField(Music, blank=True)
    height = models.ForeignKey(
        Height, blank=True, null=True, verbose_name="Height", on_delete=models.CASCADE
    )
    age = models.ForeignKey(
        Age, blank=True, null=True, verbose_name="Age", on_delete=models.CASCADE
    )
    tvShows = models.ManyToManyField(TvShows, blank=True)
    sportsTeams = models.ManyToManyField(SportsTeams, blank=True)
    movies = models.ManyToManyField(Movies, blank=True)
    work = models.CharField(max_length=265, null=True, blank=True)
    book = models.ManyToManyField(Book, blank=True)
    likes = models.ManyToManyField("self", blank=True, related_name="author")
    photos_quota = models.SmallIntegerField(default=3)
    # avatar = models.TextField(null=True, blank=True)
    avatar_index = models.IntegerField(default=0)
    owned_by = models.ManyToManyField(
        "User", blank=True, related_name="fake_users")
    broadcast_read_upto = models.IntegerField(default=0)  # id of broadcast
    broadcast_deleted_upto = models.IntegerField(default=0)  # id of broadcast
    firstmessage_read_upto = models.IntegerField(
        default=0)  # id of firstmessage

    onesignal_player_id = models.CharField(
        max_length=256, blank=True, null=True)
    roles = models.ManyToManyField(
        "UserRole", related_name="users", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    user_last_seen = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    notification_sent = models.BooleanField(
        default=False, null=True, blank=True)
    notified_count = models.IntegerField(default=0, null=True, blank=True)
    paste_access = models.BooleanField(default=False, null=True, blank=True)
    # allow_manual_chat = models.BooleanField(default=False, null=True, blank=True)
    zip_code = models.CharField(
        max_length=50, default=None, null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_purchase_coins = self.purchase_coins
        self.__original_gift_coins = self.gift_coins
        if not self.fullName:
            char_to_be_removed = ["@", "i69app.com", "gmail.com", ".com"]
            name = self.username
            for char in char_to_be_removed:
                name = name.replace(char, "")
            self.fullName = name

    def save(self, *args, **kwargs):
        thread_local = RequestMiddleware.thread_local
        if hasattr(thread_local, "current_user"):
            user = thread_local.current_user
        else:
            user = None
        if (
            self.__original_purchase_coins != self.purchase_coins
            or self.__original_gift_coins != self.gift_coins
        ):
            print("changed")
            CoinsHistory(
                user_id=self.id,
                actor=user,
                purchase_coins=self.purchase_coins,
                gift_coins=self.gift_coins,
            ).save()
        super().save(*args, **kwargs)

    def deductCoins(self, value, description=""):
        if self.coins >= value:
            if self.purchase_coins >= value:
                self.purchase_coins = self.purchase_coins - value
            elif self.gift_coins + self.purchase_coins >= value:
                self.purchase_coins = 0
                self.gift_coins = self.gift_coins + self.purchase_coins - value
            else:
                raise Exception("Not enough coins.")

            # save the coin spending history
            coin_spending_history = CoinSpendingHistory()
            coin_spending_history.user = self
            coin_spending_history.coins_spent = value
            coin_spending_history.description = description
            coin_spending_history.save()
        else:
            raise Exception("Not enough coins..")

    def addCoins(self, value):
        self.purchase_coins = self.purchase_coins + value
        self.purchase_coins_date = datetime.now()
        return

    def get_coinsettings_region(self):
        if self.country_code == None:
            user_region = None
        else:
            user_country = Country.objects.filter(
                name=self.country_code.upper())
            if user_country.count():
                user_region = CoinSettingsRegion.objects.filter(
                    countries=user_country[0]
                )
                if user_region.count():
                    user_region = user_region[0]
                else:
                    user_region = None
            else:
                user_region = None

        return user_region
    
    def get_language_id_code(self):
        lang_code = self.language.first().language_code.upper() + "-" if self.language.first() and self.language.first().language_code  else None
        language_id_code = f"{lang_code}{self.worker_id_code:07n}" if lang_code is not None else None
        return language_id_code
    
    @property
    def coins(self):
        return self.purchase_coins + self.gift_coins

    @property
    def is_fake(self):
        return "i69app.com" in self.email

    @property
    def subscription(self):
        if user_sub := self.user_subscription.last():
            return user_sub.subscription.name

    def avatar(self):
        try:
            return self.avatar_photos.all()[self.avatar_index]
        except:
            try:
                return self.avatar_photos.all()[0]
            except:
                return None

    def see_unseen_message_reminders(self) -> None:
        unseen_message_reminders = self.notification_set.filter(
            seen=False, notification_setting__id="MSGREMINDER"
        )
        unseen_message_reminders.update(seen=True)

    @property
    def interestedIn_display(self):
        return (
            list(map(int, self.interested_in.split(","))
                 ) if self.interested_in else []
        )

    def last_seen(self):
        return cache.get("seen_%s" % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.now()
            if now > self.last_seen() + timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def image_tag(self):
        return '<img src="%s" />'

    def socialProvider(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT provider FROM social_auth_usersocialauth where user_id=%s",
            [str(self.id).replace("-", "")],
        )
        row = cursor.fetchone()
        if row == None:
            return ""
        else:
            return format_html(
                '<img style="width: 25px;height: 25px;" src="/static/admin/img/{}.png">',
                row[0].split("-")[0],
            )

    socialProvider.short_description = "Provider"
    socialProvider.allow_tags = True
    avatar.short_description = "Image"
    avatar.allow_tags = True

    def has_blocked(self, target: User) -> bool:
        return self.blockedUsers.filter(id=target.id).exists()


def content_file_name(instance, filename):
    name, ext = filename.split(".")
    file_path = "photos/user_{user_id}/{name}.{ext}".format(
        user_id=instance.user.id,
        name=uuid.uuid4(),
        ext=ext,
    )
    return file_path


class UserPhoto(models.Model):
    file = models.ImageField(
        upload_to=content_file_name, null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="avatar_photos", null=True
    )
    is_admin_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} {self.pk}"


class PrivateUserPhoto(models.Model):
    file = models.ImageField(
        upload_to=content_file_name, null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="private_avatar_photos", null=True
    )
    is_admin_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.pk}"


class ReviewUserPhoto(models.Model):
    def content_file_review_name(instance, filename):
        return content_file_name(instance.user_photo, filename)

    user_photo = models.ForeignKey(UserPhoto, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=content_file_review_name)
    created_at = models.DateTimeField(auto_now_add=True)



class BlockedImageAlternatives(models.Model):
    image = models.ImageField(upload_to="default", null=True, blank=True)
    action = models.CharField(
        choices=(
            ("BLOCKED_IMG", "BLOCKED_IMG"),
            ("IF_NO_IMAGE", "IF_NO_IMAGE"),
            ("FEMALE", "FEMALE"),
            ("MALE", "MALE"),
            ("PREFER_NOT_TO_SAY", "PREFER_NOT_TO_SAY"),
        ),
        max_length=50,
    )

    def __str__(self):
        return f"{self.action.upper()}:  {self.image.url}"


class UserSocialProfile(models.Model):
    SOCIAL_PROFILE_PLATFORMS = (
        (1, "GOOGLE"),
        (2, "FACEBOOK"),
        (3, "INSTAGRAM"),
        (4, "SNAPCHAT"),
        (5, "LINKEDIN"),
        (6, "REDDIT"),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.PositiveSmallIntegerField(
        choices=SOCIAL_PROFILE_PLATFORMS, default=4
    )
    url = models.URLField()

    class Meta:
        verbose_name_plural = "User Social Profiles"
        verbose_name = "User Social Profile"

    def __str__(self):
        return str(self.user.username) + " - " + str(self.platform)


class Country(models.Model):
    name = models.CharField(choices=countries, max_length=50, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        for country in list(countries):
            if country[0] == self.name:
                return country[1]
        return self.name

    def save(self, *args, **kwargs):
        for country in list(countries):
            if country[0] == self.name:
                self.full_name = country[1]
        return super().save(*args, **kwargs)


class CoinSettingsRegion(models.Model):
    title = models.CharField(max_length=100, unique=True)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(CoinSettingsRegion, self).save(*args, **kwargs)

        coinsettings = CoinSettings.objects.all().order_by("id")
        regions = CoinSettingsRegion.objects.all().order_by("id")
        for cs in coinsettings:
            for reg in regions:
                coinsetting_for_region = CoinSettingsForRegion.objects.filter(
                    coinsettings=cs, region=reg)
                if coinsetting_for_region.count() == 0:
                    coinsetting_for_region = CoinSettingsForRegion()
                    coinsetting_for_region.coinsettings = cs
                    coinsetting_for_region.region = reg
                    coinsetting_for_region.coins_needed = cs.coins_needed
                    coinsetting_for_region.save()

        real_gifts = RealGift.objects.all().order_by('id')
        for r_g in real_gifts:
            for reg in regions:
                realgift_price_for_region = RealGiftPriceForRegion.objects.filter(
                    real_gift=r_g, region=reg)
                if realgift_price_for_region.count() == 0:
                    realgift_price_for_region = RealGiftPriceForRegion()
                    realgift_price_for_region.real_gift = r_g
                    realgift_price_for_region.region = reg
                    realgift_price_for_region.cost = r_g.cost
                    realgift_price_for_region.save()

        virtual_gifts = VirtualGift.objects.all().order_by('id')
        for v_g in virtual_gifts:
            for reg in regions:
                virtualgift_price_for_region = VirtualGiftPriceForRegion.objects.filter(
                    virtual_gift=v_g, region=reg)
                if virtualgift_price_for_region.count() == 0:
                    virtualgift_price_for_region = VirtualGiftPriceForRegion()
                    virtualgift_price_for_region.virtual_gift = v_g
                    virtualgift_price_for_region.region = reg
                    virtualgift_price_for_region.cost = v_g.cost
                    virtualgift_price_for_region.save()

        coin_prices = CoinPrices.objects.all().order_by('id')
        for coin_price in coin_prices:
            for reg in regions:
                coin_price_for_region = CoinPricesForRegion.objects.filter(
                    coin_price=coin_price, region=reg)
                if coin_price_for_region.count() == 0:
                    coin_price_for_region = CoinPricesForRegion()
                    coin_price_for_region.coin_price = coin_price
                    coin_price_for_region.region = reg
                    coin_price_for_region.coins_count = coin_price.coins_count
                    coin_price_for_region.original_price = coin_price.original_price
                    coin_price_for_region.discounted_price = coin_price.discounted_price
                    coin_price_for_region.save()

        purchase_plans = Plan.objects.all().order_by('id')
        for plan in purchase_plans:
            for reg in regions:
                plan_for_region = PlanForRegion.objects.filter(
                    plan=plan, region=reg)
                if plan_for_region.count() == 0:
                    plan_for_region = PlanForRegion()
                    plan_for_region.plan = plan
                    plan_for_region.region = reg
                    plan_for_region.price_in_coins = plan.price_in_coins
                    plan_for_region.is_active = plan.is_active
                    plan_for_region.save()


class CoinSettings(models.Model):
    method = models.CharField(max_length=70)
    coins_needed = models.IntegerField()

    def __str__(self):
        return self.method + " --- " + str(self.coins_needed)


class CoinSettingsForRegion(models.Model):
    coinsettings = models.ForeignKey(CoinSettings, on_delete=models.CASCADE)
    region = models.ForeignKey(CoinSettingsRegion, on_delete=models.CASCADE)
    coins_needed = models.IntegerField()

    def __str__(self):
        return self.coinsettings.method + " (" + self.region.title + ")"


class CoinsHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="coin_holder")
    actor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="coin_editor", null=True
    )
    purchase_coins = models.IntegerField()
    gift_coins = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"


class CoinsHistorys(User):
    class Meta:
        proxy = True


class ModeratorQue(models.Model):
    moderator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fake_user"
    )
    worker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="active_worker", null=True
    )
    isAssigned = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.moderator} : {self.worker} : {self.isAssigned}"


class ModeratorQScheduler(models.Model):
    ModeratorQueSchedulerChoices = (
        ("moderator_logout_intervel", "moderator_logout_intervel"),
        (
            "unassign_moderator_from_inactive_to_active_worker_intervel",
            "unassign_moderator_from_inactive_to_active_worker_intervel",
        ),
    )
    IntervalPeriodChoices = (
        ("Days", "Days"),
        ("Hours", "Hours"),
        ("Minutes", "Minutes"),
        ("Seconds", "Seconds"),
    )
    taskName = models.CharField(
        choices=ModeratorQueSchedulerChoices, max_length=100)
    numberOfPeriods = models.IntegerField(default=0)
    intervalPeriod = models.CharField(
        choices=IntervalPeriodChoices, max_length=100)

    def __str__(self):
        return f"{self.taskName} - {self.numberOfPeriods} - {self.intervalPeriod}"


class ChatsQueSetting(models.Model):
    ModeratorQueSchedulerChoices = (
        ("inactive_worker_logout_intervel", "inactive_worker_logout_intervel"),
        (
            "unassign_chat_from_inactive_worker_to_active_worker_intervel",
            "unassign_chat_from_inactive_worker_to_active_worker_intervel",
        ),
    )
    IntervalPeriodChoices = (
        ("Days", "Days"),
        ("Hours", "Hours"),
        ("Minutes", "Minutes"),
        ("Seconds", "Seconds"),
    )
    taskName = models.CharField(
        choices=ModeratorQueSchedulerChoices, max_length=100)
    numberOfPeriods = models.IntegerField()
    intervalPeriod = models.CharField(
        choices=IntervalPeriodChoices, max_length=100)

    def __str__(self):
        return f"{self.taskName} - {self.numberOfPeriods} - {self.intervalPeriod}"


class ChatsQue(models.Model):
    room_id = models.IntegerField()
    moderator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_fake_user"
    )
    worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_active_worker",
        blank=True,
        null=True,
    )
    isAssigned = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-isAssigned", "date_created")

    def __str__(self):
        return f"room-id: {self.room_id} : {self.moderator} : {self.worker} : {self.isAssigned}"


class ModeratorOnlineScheduler(models.Model):
    list_name = models.CharField(max_length=70)
    online_time = models.TimeField(auto_now_add=False, blank=True, null=True)
    offline_time = models.TimeField(auto_now_add=False, blank=True, null=True)
    moderator_list = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.list_name} : online at {self.online_time} and offline at {self.offline_time}"


class UserLimit(models.Model):
    ActionChoices = (
        ("MultiStoryLimit", "MultiStoryLimit"),
        ("FreeProfilePhotos", "FreeProfilePhotos"),
    )
    action_name = models.CharField(
        choices=ActionChoices, max_length=95, unique=True)
    limit_value = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.action_name + " limit: " + str(self.limit_value)


class PrivatePhotoViewTime(models.Model):
    no_of_hours = models.IntegerField()

    def __str__(self):
        return f"Private Photo will be available for {self.no_of_hours} Hours after the time of acception."


class PrivatePhotoViewRequest(models.Model):
    user_to_view = models.ForeignKey(
        User, related_name="user_to_view", on_delete=models.CASCADE
    )
    requested_user = models.ForeignKey(
        User, related_name="requested_user", on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ("A", "APPROVE"),
            ("R", "REJECT"),
            ("P", "PENDING"),
            ("C", "CANCEL"),
        ),
        default="P",
    )

    def __str__(self):
        return f"{self.requested_user.fullName} -> request to view -> {self.user_to_view.fullName}"


class Settings(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)
    # group = models.CharField(max_length=255)
    description = models.CharField(
        max_length=255, null=True, default=None, blank=True)

    @classmethod
    def get_setting(cls, key, default=None):
        try:
            obj = cls.objects.filter(key=key).first()
            if obj:
                return obj.value
            return default
        except Exception:
            return default

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def __str__(self) -> str:
        return f"{self.key}"


class DeleteAccountSetting(models.Model):
    is_delete_account_allowed = models.BooleanField(default=True)


class FailedFCMMessage(models.Model):
    gcm_device = models.ForeignKey(GCMDevice, on_delete=models.CASCADE)
    error_message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.gcm_device.id} ({self.gcm_device.user.username})"


class ProfileFollow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_following')
    created_at = models.DateTimeField(auto_now=True)


class ProfileVisit(models.Model):
    visitor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_visitor')
    visiting = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_visiting')
    created_at = models.DateTimeField(auto_now=True)
    last_visited_at = models.DateTimeField(null=True)

    @property
    def last_visited(self):
        return self.last_visited_at or self.created_at

    @property
    def can_notify_profile_visit(self):
        if not self.last_visited_at:
            # First time visiting
            return True
        # Will return True only of the time between the last visit and now is greater than the specified setting
        print("++++++++++++++++++++++++++++++++++",  self.last_visited)
        print("++++++++++++++++++++++++++++++++++",  timezone.now())
        print(timezone.now() > self.last_visited + timedelta(minutes=settings.PROFILE_VISIT_NOTIFICATION_TIMEOUT))
        return timezone.now() > self.last_visited + timedelta(minutes=settings.PROFILE_VISIT_NOTIFICATION_TIMEOUT)


class FeatureSettings(models.Model):
    CHOICES = (
        (0, "OFF"),
        (1, "ON"),
    )

    description = models.CharField(
        max_length=255, null=True, default=None, blank=True)
    feature_type = models.CharField(max_length=255, unique=True)
    feature_status = models.PositiveSmallIntegerField(
        choices=CHOICES, default=0)

    @classmethod
    def get_setting(cls, feature_type, default=0):
        try:
            obj = cls.objects.filter(feature_type=feature_type).first()
            if obj:
                return obj.feature_status
            return default
        except Exception:
            return default

    class Meta:
        verbose_name = "Feature Setting"
        verbose_name_plural = "Feature Settings"

    def __str__(self) -> str:
        return f"{self.feature_type}"


class CoinSpendingHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_coin_spending_history')
    coins_spent = models.IntegerField()
    description = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Coin Spending History"
        verbose_name_plural = "Coin Spending History"


class UserProfileTranlations(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_fr = models.CharField(max_length=255, null=True, blank=True)
    name_zh_cn = models.CharField(max_length=255, null=True, blank=True)
    name_nl = models.CharField(max_length=255, null=True, blank=True)
    name_de = models.CharField(max_length=255, null=True, blank=True)
    name_sw = models.CharField(max_length=255, null=True, blank=True)
    name_it = models.CharField(max_length=255, null=True, blank=True)
    name_ar = models.CharField(max_length=255, null=True, blank=True)
    name_iw = models.CharField(max_length=255, null=True, blank=True)
    name_ja = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)
    name_fa = models.CharField(max_length=255, null=True, blank=True)
    name_pt_br = models.CharField(max_length=255, null=True, blank=True)
    name_pt_pt = models.CharField(max_length=255, null=True, blank=True)
    name_es = models.CharField(max_length=255, null=True, blank=True)
    # manually translate due to unavailability in google
    name_es_419 = models.CharField(max_length=255, null=True, blank=True)
    name_el = models.CharField(max_length=255, null=True, blank=True)
    name_zh_tw = models.CharField(max_length=255, null=True, blank=True)
    name_uk = models.CharField(max_length=255, null=True, blank=True)
    name_ko = models.CharField(max_length=255, null=True, blank=True)
    # manually translate due to unavailability in google
    name_br = models.CharField(max_length=255, null=True, blank=True)
    name_pl = models.CharField(max_length=255, null=True, blank=True)
    name_vi = models.CharField(max_length=255, null=True, blank=True)
    # manually translate due to unavailability in google
    name_nn = models.CharField(max_length=255, null=True, blank=True)
    name_no = models.CharField(max_length=255, null=True, blank=True)
    name_sv = models.CharField(max_length=255, null=True, blank=True)
    name_hr = models.CharField(max_length=255, null=True, blank=True)
    name_cs = models.CharField(max_length=255, null=True, blank=True)
    name_da = models.CharField(max_length=255, null=True, blank=True)
    name_tl = models.CharField(max_length=255, null=True, blank=True)
    name_fi = models.CharField(max_length=255, null=True, blank=True)
    name_sl = models.CharField(max_length=255, null=True, blank=True)
    name_sq = models.CharField(max_length=255, null=True, blank=True)
    name_am = models.CharField(max_length=255, null=True, blank=True)
    name_hy = models.CharField(max_length=255, null=True, blank=True)
    name_la = models.CharField(max_length=255, null=True, blank=True)
    name_lv = models.CharField(max_length=255, null=True, blank=True)
    name_th = models.CharField(max_length=255, null=True, blank=True)
    name_az = models.CharField(max_length=255, null=True, blank=True)
    name_eu = models.CharField(max_length=255, null=True, blank=True)
    name_be = models.CharField(max_length=255, null=True, blank=True)
    name_bn = models.CharField(max_length=255, null=True, blank=True)
    name_bs = models.CharField(max_length=255, null=True, blank=True)
    name_bg = models.CharField(max_length=255, null=True, blank=True)
    name_km = models.CharField(max_length=255, null=True, blank=True)
    name_ca = models.CharField(max_length=255, null=True, blank=True)
    name_et = models.CharField(max_length=255, null=True, blank=True)
    name_gl = models.CharField(max_length=255, null=True, blank=True)
    name_ka = models.CharField(max_length=255, null=True, blank=True)
    name_hi = models.CharField(max_length=255, null=True, blank=True)
    name_hu = models.CharField(max_length=255, null=True, blank=True)
    name_is = models.CharField(max_length=255, null=True, blank=True)
    name_id = models.CharField(max_length=255, null=True, blank=True)
    name_ga = models.CharField(max_length=255, null=True, blank=True)
    name_mk = models.CharField(max_length=255, null=True, blank=True)
    name_mn = models.CharField(max_length=255, null=True, blank=True)
    name_ne = models.CharField(max_length=255, null=True, blank=True)
    name_ro = models.CharField(max_length=255, null=True, blank=True)
    name_sr = models.CharField(max_length=255, null=True, blank=True)
    name_sk = models.CharField(max_length=255, null=True, blank=True)
    name_ta = models.CharField(max_length=255, null=True, blank=True)
    name_tg = models.CharField(max_length=255, null=True, blank=True)
    name_tr = models.CharField(max_length=255, null=True, blank=True)
    name_ur = models.CharField(max_length=255, null=True, blank=True)
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        for lang in SUPPORTED_LANGUAGES:
            lang_str = lang
            if "-" in lang_str:
                lang_str = lang_str.replace("-", "_")
            name_field = "name_%s" % lang_str
            setattr(
                self,
                name_field,
                language_translate(getattr(self, name_field), self.name, lang)
            )

        return super().save(*args, **kwargs)


class SetInterestedInRegion(models.Model):
    title = models.CharField(max_length=100, unique=True)
    countries = models.ManyToManyField(Country)

    def __str__(self):
        return self.title


class UserInterestedIn(models.Model):
    InterestChoices = (
        ("SERIOUS_RELATIONSHIP", "SERIOUS RELATIONSHIP"),
        ("CAUSAL_DATING", "CAUSAL DATING"),
        ("NEW_FRIENDS", "NEW FRIENDS"),
        ("ROOM_MATES", "ROOM MATES"),
        ("BUSINESS_CONTACTS", "BUSINESS CONTACTS"),
    )
    category_name = models.CharField(
        max_length=95, unique=True, choices=InterestChoices)
    str_name = models.CharField(max_length=95, blank=True, null=True)
    str_name_fr = models.CharField(max_length=65, null=True, blank=True)
    str_name_zh_cn = models.CharField(max_length=65, null=True, blank=True)
    str_name_nl = models.CharField(max_length=65, null=True, blank=True)
    str_name_de = models.CharField(max_length=65, null=True, blank=True)
    str_name_sw = models.CharField(max_length=65, null=True, blank=True)
    str_name_it = models.CharField(max_length=65, null=True, blank=True)
    str_name_ar = models.CharField(max_length=65, null=True, blank=True)
    str_name_iw = models.CharField(max_length=65, null=True, blank=True)
    str_name_ja = models.CharField(max_length=65, null=True, blank=True)
    str_name_ru = models.CharField(max_length=65, null=True, blank=True)
    str_name_fa = models.CharField(max_length=65, null=True, blank=True)
    str_name_pt_br = models.CharField(max_length=65, null=True, blank=True)
    str_name_pt_pt = models.CharField(max_length=65, null=True, blank=True)
    str_name_es = models.CharField(max_length=65, null=True, blank=True)
    str_name_es_419 = models.CharField(max_length=65, null=True,
                                       blank=True)  # manually translate due to unavailability in google
    str_name_el = models.CharField(max_length=65, null=True, blank=True)
    str_name_zh_tw = models.CharField(max_length=65, null=True, blank=True)
    str_name_uk = models.CharField(max_length=65, null=True, blank=True)
    str_name_ko = models.CharField(max_length=65, null=True, blank=True)
    str_name_br = models.CharField(max_length=65, null=True,
                                   blank=True)  # manually translate due to unavailability in google
    str_name_pl = models.CharField(max_length=65, null=True, blank=True)
    str_name_vi = models.CharField(max_length=65, null=True, blank=True)
    str_name_nn = models.CharField(max_length=65, null=True,
                                   blank=True)  # manually translate due to unavailability in google
    str_name_no = models.CharField(max_length=65, null=True, blank=True)
    str_name_sv = models.CharField(max_length=65, null=True, blank=True)
    str_name_hr = models.CharField(max_length=65, null=True, blank=True)
    str_name_cs = models.CharField(max_length=65, null=True, blank=True)
    str_name_da = models.CharField(max_length=65, null=True, blank=True)
    str_name_tl = models.CharField(max_length=65, null=True, blank=True)
    str_name_fi = models.CharField(max_length=65, null=True, blank=True)
    str_name_sl = models.CharField(max_length=65, null=True, blank=True)
    str_name_sq = models.CharField(max_length=65, null=True, blank=True)
    str_name_am = models.CharField(max_length=65, null=True, blank=True)
    str_name_hy = models.CharField(max_length=65, null=True, blank=True)
    str_name_la = models.CharField(max_length=65, null=True, blank=True)
    str_name_lv = models.CharField(max_length=65, null=True, blank=True)
    str_name_th = models.CharField(max_length=65, null=True, blank=True)
    str_name_az = models.CharField(max_length=65, null=True, blank=True)
    str_name_eu = models.CharField(max_length=65, null=True, blank=True)
    str_name_be = models.CharField(max_length=65, null=True, blank=True)
    str_name_bn = models.CharField(max_length=65, null=True, blank=True)
    str_name_bs = models.CharField(max_length=65, null=True, blank=True)
    str_name_bg = models.CharField(max_length=65, null=True, blank=True)
    str_name_km = models.CharField(max_length=65, null=True, blank=True)
    str_name_ca = models.CharField(max_length=65, null=True, blank=True)
    str_name_et = models.CharField(max_length=65, null=True, blank=True)
    str_name_gl = models.CharField(max_length=65, null=True, blank=True)
    str_name_ka = models.CharField(max_length=65, null=True, blank=True)
    str_name_hi = models.CharField(max_length=65, null=True, blank=True)
    str_name_hu = models.CharField(max_length=65, null=True, blank=True)
    str_name_is = models.CharField(max_length=65, null=True, blank=True)
    str_name_id = models.CharField(max_length=65, null=True, blank=True)
    str_name_ga = models.CharField(max_length=65, null=True, blank=True)
    str_name_mk = models.CharField(max_length=65, null=True, blank=True)
    str_name_mn = models.CharField(max_length=65, null=True, blank=True)
    str_name_ne = models.CharField(max_length=65, null=True, blank=True)
    str_name_ro = models.CharField(max_length=65, null=True, blank=True)
    str_name_sr = models.CharField(max_length=65, null=True, blank=True)
    str_name_sk = models.CharField(max_length=65, null=True, blank=True)
    str_name_ta = models.CharField(max_length=65, null=True, blank=True)
    str_name_tg = models.CharField(max_length=65, null=True, blank=True)
    str_name_tr = models.CharField(max_length=65, null=True, blank=True)
    str_name_ur = models.CharField(max_length=65, null=True, blank=True)
    str_name_uz = models.CharField(max_length=65, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.str_name = self.category_name.replace("_", " ")
        for lang in SUPPORTED_LANGUAGES:
            lang_str = lang
            if "-" in lang_str:
                lang_str = lang_str.replace("-", "_")
            name_field = "str_name_%s" % lang_str
            setattr(
                self,
                name_field,
                language_translate(getattr(self, name_field),
                                   self.str_name, lang)
            )
        return super().save(*args, **kwargs)


class HideUserInterestedIn(models.Model):
    category = models.ForeignKey(
        UserInterestedIn, on_delete=models.CASCADE
    )
    region = models.ManyToManyField(Country)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category.category_name


class UserInterestForRegion(models.Model):
    user_interested_in = models.ForeignKey(
        UserInterestedIn, on_delete=models.CASCADE)
    region = models.ForeignKey(SetInterestedInRegion, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_interested_in.str_name + " (" + self.region.title + ")"

    class Meta:
        unique_together = ('user_interested_in', 'region')


class ErrorMessageTranslation(models.Model):
    message = models.CharField(max_length=255, unique=True)
    message_fr = models.CharField(max_length=255, null=True, blank=True)
    message_zh_cn = models.CharField(max_length=255, null=True, blank=True)
    message_nl = models.CharField(max_length=255, null=True, blank=True)
    message_de = models.CharField(max_length=255, null=True, blank=True)
    message_sw = models.CharField(max_length=255, null=True, blank=True)
    message_it = models.CharField(max_length=255, null=True, blank=True)
    message_ar = models.CharField(max_length=255, null=True, blank=True)
    message_iw = models.CharField(max_length=255, null=True, blank=True)
    message_ja = models.CharField(max_length=255, null=True, blank=True)
    message_ru = models.CharField(max_length=255, null=True, blank=True)
    message_fa = models.CharField(max_length=255, null=True, blank=True)
    message_pt_br = models.CharField(max_length=255, null=True, blank=True)
    message_pt_pt = models.CharField(max_length=255, null=True, blank=True)
    message_es = models.CharField(max_length=255, null=True, blank=True)
    # manually translate due to unavailability in google
    message_es_419 = models.CharField(max_length=255, null=True, blank=True)
    message_el = models.CharField(max_length=255, null=True, blank=True)
    message_zh_tw = models.CharField(max_length=255, null=True, blank=True)
    message_uk = models.CharField(max_length=255, null=True, blank=True)
    message_ko = models.CharField(max_length=255, null=True, blank=True)
    # manually translate due to unavailability in google
    message_br = models.CharField(max_length=255, null=True, blank=True)
    message_pl = models.CharField(max_length=255, null=True, blank=True)
    message_vi = models.CharField(max_length=255, null=True, blank=True)
    # manually translate due to unavailability in google
    message_nn = models.CharField(max_length=255, null=True, blank=True)
    message_no = models.CharField(max_length=255, null=True, blank=True)
    message_sv = models.CharField(max_length=255, null=True, blank=True)
    message_hr = models.CharField(max_length=255, null=True, blank=True)
    message_cs = models.CharField(max_length=255, null=True, blank=True)
    message_da = models.CharField(max_length=255, null=True, blank=True)
    message_tl = models.CharField(max_length=255, null=True, blank=True)
    message_fi = models.CharField(max_length=255, null=True, blank=True)
    message_sl = models.CharField(max_length=255, null=True, blank=True)
    message_sq = models.CharField(max_length=255, null=True, blank=True)
    message_am = models.CharField(max_length=255, null=True, blank=True)
    message_hy = models.CharField(max_length=255, null=True, blank=True)
    message_la = models.CharField(max_length=255, null=True, blank=True)
    message_lv = models.CharField(max_length=255, null=True, blank=True)
    message_th = models.CharField(max_length=255, null=True, blank=True)
    message_az = models.CharField(max_length=255, null=True, blank=True)
    message_eu = models.CharField(max_length=255, null=True, blank=True)
    message_be = models.CharField(max_length=255, null=True, blank=True)
    message_bn = models.CharField(max_length=255, null=True, blank=True)
    message_bs = models.CharField(max_length=255, null=True, blank=True)
    message_bg = models.CharField(max_length=255, null=True, blank=True)
    message_km = models.CharField(max_length=255, null=True, blank=True)
    message_ca = models.CharField(max_length=255, null=True, blank=True)
    message_et = models.CharField(max_length=255, null=True, blank=True)
    message_gl = models.CharField(max_length=255, null=True, blank=True)
    message_ka = models.CharField(max_length=255, null=True, blank=True)
    message_hi = models.CharField(max_length=255, null=True, blank=True)
    message_hu = models.CharField(max_length=255, null=True, blank=True)
    message_is = models.CharField(max_length=255, null=True, blank=True)
    message_id = models.CharField(max_length=255, null=True, blank=True)
    message_ga = models.CharField(max_length=255, null=True, blank=True)
    message_mk = models.CharField(max_length=255, null=True, blank=True)
    message_mn = models.CharField(max_length=255, null=True, blank=True)
    message_ne = models.CharField(max_length=255, null=True, blank=True)
    message_ro = models.CharField(max_length=255, null=True, blank=True)
    message_sr = models.CharField(max_length=255, null=True, blank=True)
    message_sk = models.CharField(max_length=255, null=True, blank=True)
    message_ta = models.CharField(max_length=255, null=True, blank=True)
    message_tg = models.CharField(max_length=255, null=True, blank=True)
    message_tr = models.CharField(max_length=255, null=True, blank=True)
    message_ur = models.CharField(max_length=255, null=True, blank=True)
    message_uz = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        for lang in SUPPORTED_LANGUAGES:
            lang_str = lang
            if "-" in lang_str:
                lang_str = lang_str.replace("-", "_")
            message_field = "message_%s" % lang_str
            setattr(
                self,
                message_field,
                language_translate(
                    getattr(self, message_field), self.message, lang)
            )

        return super().save(*args, **kwargs)


class UserForModsRestriction(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='restricted_user_for_mods')
    moderators = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class InstagramScrapy(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    followers = models.CharField(max_length=100, null=True, blank=True)
    following = models.CharField(max_length=100, null=True, blank=True)
    full_name =  models.CharField(max_length=100, null=True, blank=True)
    total_posts =  models.CharField(max_length=100, null=True, blank=True)
    posts_data = models.JSONField(null=True, blank=True)
    profile_picture = models.CharField(max_length=1000, null=True, blank=True)