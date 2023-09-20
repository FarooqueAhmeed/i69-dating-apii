import math
import traceback
from typing import List, Optional, Union

from django.contrib.auth import get_user_model
from django.db import connection
from django.db.models import F, Q
from geopy.geocoders import Nominatim, ArcGIS
from push_notifications.models import GCMDevice
from .models import User, FailedFCMMessage, ErrorMessageTranslation
from defaultPicker.utils import translated_field_name, custom_translate
import json

GENDER_CHOICE__MAP = {0: "Male", 1: "Female"}

AGE_RANGE = (
    (0, "18"),
    (1, "19"),
    (2, "20"),
    (3, "21"),
    (4, "22"),
    (5, "23"),
    (6, "24"),
    (7, "25"),
    (8, "26"),
    (9, "27"),
    (10, "28"),
    (11, "29"),
    (12, "30"),
    (13, "31"),
    (14, "32"),
    (15, "33"),
    (16, "34"),
    (17, "35"),
    (18, "36"),
    (19, "37"),
    (20, "38"),
    (21, "39"),
    (22, "40"),
    (23, "41"),
    (24, "42"),
    (25, "43"),
    (26, "44"),
    (27, "45"),
    (28, "46"),
    (29, "47"),
    (30, "48"),
    (31, "49"),
    (32, "50"),
    (33, "51"),
    (34, "52"),
    (35, "53"),
    (36, "54"),
    (37, "55"),
    (38, "56"),
    (39, "57"),
    (40, "58"),
    (41, "59"),
)


def get_domain_url_from_context(info):
    headers = dict(info.context['headers'])
    host = headers.get(b'host', b'').decode('utf-8')
    proto = headers.get(b'x-forwarded-proto', b'http').decode('utf-8')

    domain_url = f"{proto}://{host}"
    return domain_url


def get_gender_from_code(id: int) -> Optional[str]:
    try:
        return GENDER_CHOICE__MAP[id]
    except Exception:
        return None


def parse_lat_long_string(lat_long: str = None):
    try:
        return list(map(float, lat_long.split(",")))
    except Exception:
        return None, None


def get_zipcode(latitude, longitude):
    """
    latitude = 40.7128
    longitude = -74.0060
    zipcode = get_zipcode(latitude, longitude)
    print(zipcode)
    """
    try:
        geolocator = Nominatim(user_agent="framework")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.raw.get('address')
        if address and address.get('postcode'):
            return address.get('postcode')
        
        geolocator2 = ArcGIS(user_agent="framework")
        location2 = geolocator2.reverse((latitude, longitude), exactly_one=True)
        if location.raw.get('Postal'):
            return location.raw.get('Postal')
    except Exception as e:
        print(e)
        return ""
    return "NA"


def get_country_from_geo_point(geo_point: Union[List[float], str] = None) -> tuple:
    try:
        if isinstance(geo_point, str):
            geo_point = parse_lat_long_string(lat_long=geo_point)
        geolocator = Nominatim(user_agent="framework")
        location = geolocator.reverse(f"{geo_point[0]},{geo_point[1]}", language="en")
        address = location.raw.get("address", {})
        country = address.get("country", None)
        country_code = address.get("country_code", None)
        state = address.get("state", None)
        city = next(
            iter(
                [
                    address.get(c, None)
                    for c in ["city", "county", "state_district", "town", "village"]
                    if address.get(c, None) is not None
                ]
            ),
            None,
        )
        if not address.get('postcode'):
            geolocator2 = ArcGIS(user_agent="framework")
            location2 = geolocator.reverse(f"{geo_point[0]},{geo_point[1]}", language="en")
            zipcode = location.raw.get('Postal')
        else:
            zipcode = address.get('postcode')
        if zipcode and (zipcode not in city):
            city = f"{city}-{zipcode}"      

        # print(json.dumps(address, indent=4))
        return country, country_code, state, city, zipcode
    except Exception as e:
        print(e)
        return None, None, None, None, None


def haversine_distance(coord_one: tuple, coord_two: tuple, unit="km"):

    lon1, lat1 = coord_one
    lon2, lat2 = coord_two

    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c
    km = meters / 1000.0

    meters = round(meters, 3)
    km = round(km, 3)
    miles = km * 0.621371
    if unit == "km":
        return km
    return meters, km, miles


def get_near_by_users(user_id=None, distance_km=None):
    current_user = get_user_model().objects.filter(id=user_id).first()

    users = (
        get_user_model()
        .objects.filter(
            location__isnull=False,
            country__isnull=False,
            country=current_user.country,
            is_staff=False,
            owned_by=None,
        )
        .filter(~Q(location=""))
        .exclude(
            Q(location="")
            | Q(id=user_id)
            | Q(roles__role__in=["CHATTER", "ADMIN", "MODERATOR"])
        )
        .values("id", "country", "location")
    )

    # print(f"Query: {users.query}")

    # users = users.filter(~Q(location=""))

    # users = users.exclude(location="", id=user_id, roles__role__in=["CHATTER", "ADMIN", "MODERATOR"]).values(
    #     "id", "country", "location"
    # )

    if not current_user.location:
        return []

    if current_user.notified_count > 0:
        print("Notifications Already sent to nearby users")
        return []

    start_point = parse_lat_long_string(lat_long=current_user.location)
    final_users = []
    for user in users:
        try:
            distance = haversine_distance(
                coord_one=start_point,
                coord_two=parse_lat_long_string(lat_long=user["location"]),
            )
            final_users.append({"id": user["id"], "distance": float(distance)})
        except Exception as e:
            print(e)
    # print(f"Final Users With Distance: {final_users}")
    final_users = [fu for fu in final_users if fu["distance"] < float(distance_km)]
    final_users = sorted(final_users, key=lambda item: item["distance"], reverse=False)
    # print(f"Final Users: {final_users}")
    return final_users


def get_setting(key: str = None):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT title,title_fr,message_str,message_str_fr FROM chat_notificationsettings WHERE id=%s;",
            [key],
        )
        row = cursor.fetchone()
    return row


def notifiy_near_by_users(user_id, distance_km=50000):
    try:
        users = get_near_by_users(user_id=user_id, distance_km=distance_km)
        # print(f"Users: {users}")
        if len(users) > 0:
            user_ids = [str(user["id"]) for user in users]
            # print(f"User Ids: {user_ids}, Current User: {user_id}")

            currnet_device_ids = GCMDevice.objects.filter(user_id=user_id).values_list(
                "registration_id", flat=True
            )
            currnet_device_ids = [str(id) for id in currnet_device_ids]
            print(f"currnet_device_ids: {currnet_device_ids}")

            fcm_devices = (
                GCMDevice.objects.filter(
                    user_id__in=user_ids,
                    active=True,
                )
                .filter(~Q(registration_id__in=currnet_device_ids))
                .all()
                .distinct("registration_id")
            )

            # .filter(~Q(registration_id__in=[str(id) for id in GCMDevice.objects.filter(user_id=user_id).values_list('registration_id', flat=True).all()]))

            # fcm_devices =

            if fcm_devices.count() > 0:
                user = get_user_model().objects.filter(id=user_id).first()
                noti_sett = get_setting(key="USERJOINED")
                username = user.fullName or user.username
                title_en = f"{username} near to you has joined the app"
                title_fr = f"{username} près de chez vous a rejoint l'application"
                message_en = f"{username} near to you has joined the app"
                message_fr = f"{username} près de chez vous a rejoint l'application"
                if noti_sett:
                    title_en = f"{username} {noti_sett[0]}"
                    title_fr = f"{username} {noti_sett[1]}"
                    message_en = f"{username} {noti_sett[2]}"
                    message_fr = f"{username} {noti_sett[3]}"

                title = title_en if user.user_language_code == "en" else title_fr
                message = message_en if user.user_language_code == "en" else message_fr
                if user.notification_sent == False:
                    try:
                        resp = fcm_devices.send_message(
                            message,
                            badge=1,
                            sound="default",
                            extra={
                                "title": title,
                                "icon": None,
                                "data": {"notification_type": "SM", "img_url": None},
                                "image": None,
                                "user_id": str(user_id),
                            },
                        )
                        print(f"New user notification response: {resp}")
                        if resp[0]["success"] > 0:
                            get_user_model().objects.filter(id=user_id).update(
                                notified_count=F("notified_count") + 1,
                                notification_sent=True,
                            )
                    except Exception as ex:
                        ex = str(ex).replace("'", "\"")
                        fcm_messages = json.loads(ex)
                        for msg in fcm_messages['results']:
                            if "error" in msg:
                                print('FCM message failed. Error:', msg['error'], ', Registration ID:', msg['original_registration_id'])
                                disable_fcm_device_by_registration_id(msg['original_registration_id'], msg['error'])
                    
                return True
            else:
                print("No Devices")
                return False
        else:
            return False
    except Exception as e:
        print(e, traceback.print_exc())
        return False


def get_recipients_of_admin_realtime_notification():
    return User.objects.filter(is_active=True, is_staff=True)


def disable_fcm_device_by_registration_id(registration_id, error_message):
    gcm_device = GCMDevice.objects.filter(registration_id=registration_id).first()
    if gcm_device:
        gcm_device.active = False
        gcm_device.save()
        # print(gcm_device, gcm_device.user)

        failed_fcm = FailedFCMMessage()
        failed_fcm.gcm_device = gcm_device
        failed_fcm.error_message = error_message
        failed_fcm.save()


def translate_error_message(user, message):
    error_message = ErrorMessageTranslation.objects.filter(message__iexact=message).first()
    if not error_message:
        error_message = ErrorMessageTranslation(message=message)
        error_message.save()

    field_name = translated_field_name(user, "message")
    translated_message = getattr(error_message, field_name)

    if not translated_message or translated_message == "":
        translated_message = custom_translate(user, message)
        setattr(error_message, field_name, translated_message)
        error_message.save()

    return translated_message