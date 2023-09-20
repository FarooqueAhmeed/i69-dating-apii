from worker.models import EmailSettings
from django import forms
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.forms import fields
from django.urls import reverse
import os
from user.models import CoinSettings, CoinSettingsForRegion
import json
from .models import ContactUs
from time import gmtime, strftime
from django.core.mail import send_mail

# from asgiref.sync import async_to_sync, sync_to_async

from chat.models import Room, Message, ChatMessageImages
from user.models import User
from stock_image.models import StockImage
from django.core.files import File
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view


class ChatImagesFrm(forms.ModelForm):
    # upload_type = forms.CharField(required=True)
    class Meta:
        # To specify the model to be used to create form
        model = ChatMessageImages
        # It includes all the fields of model
        fields = "__all__"


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def chat_index(request):
    return JsonResponse({"index": "page"}, safe=False)


@csrf_exempt
@permission_classes((IsAuthenticated, ))
def image_upload(request):
    print("image upload ", request.user, request.user.is_authenticated)
    if not request.user.is_authenticated:
        return JsonResponse(
            {"success": False, "message": "You need to be logged in"}, safe=False
        )

    if request.method == "POST":
        """
        commenting below code as we can use csrf decorator to a view. Not sure why It wasn't used
        """
        # since we cant use csrf token, this is a simple way of implementing some security
        # today = int(strftime("%d", gmtime()))
        # yesterday = today - 1
        # base_check = 33333333 / 222
        # check_time = []
        # check_time.append(int(today * base_check))
        # check_time.append(int(yesterday * base_check))  # do we need this?
        # print("token: ", str(request.POST.get("token")), str(check_time))
        # print(request.POST,"===========================")
        # if not request.POST.get("token"):
        #     return JsonResponse(
        #         {"success": False, "message": "Missing token"}, safe=False
        #     )
        #
        # if not int(request.POST.get("token")) in check_time:
        #     return JsonResponse(
        #         {"success": False, "message": "Invalid token"}, safe=False
        #     )
        data = request.FILES.copy()
        imageId = request.POST.get("imageId", None)
        file = None
        if imageId:
            try:
                image = StockImage.objects.get(id=imageId)
                file = open(settings.BASE_DIR + image.file.url, "rb")
                data["image"] = File(file=file)
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, safe=False)

        form = ChatImagesFrm(request.POST, data)
        if form.is_valid():
            user = request.user
            if not user.roles.filter(role__in=["ADMIN", "CHATTER"]):
                if request.POST.get("upload_type") == "image":
                    coins = CoinSettings.objects.filter(
                        method="Photo & file - attached in Chat"
                    ).first()
                    coins_for_region = CoinSettingsForRegion.objects.filter(
                        coinsettings=coins, region=user.get_coinsettings_region()
                    )
                    if coins_for_region.count():
                        coins = coins_for_region.first()

                    if user.gift_coins + user.purchase_coins < coins.coins_needed:
                        return JsonResponse(
                            {"success": False, "message": "Insufficient coins"},
                            safe=False,
                        )
                    if coins and coins.coins_needed > 0:
                        message_coins = CoinSettings.objects.filter(
                            method="Message"
                        ).first()
                        message_coins_for_region = CoinSettingsForRegion.objects.filter(
                            coinsettings=message_coins,
                            region=user.get_coinsettings_region(),
                        )
                        if message_coins_for_region.count():
                            message_coins = message_coins_for_region.first()
                        user.deductCoins(
                            coins.coins_needed - message_coins.coins_needed, "Photo & file - attached in Chat"
                        )
                        user.save()
                elif request.POST.get("upload_type") == "video":
                    coins = CoinSettings.objects.filter(method="IMAGE").first()
                    coins_for_region = CoinSettingsForRegion.objects.filter(
                        coinsettings=coins, region=user.get_coinsettings_region()
                    )
                    if coins_for_region.count():
                        coins = coins_for_region.first()

                    if user.gift_coins + user.purchase_coins < coins.coins_needed:
                        return JsonResponse(
                            {"success": False, "message": "Insufficient coins"},
                            safe=False,
                        )
                    if coins and coins.coins_needed > 0:
                        message_coins = CoinSettings.objects.filter(
                            method="Message"
                        ).first()
                        message_coins_for_region = CoinSettingsForRegion.objects.filter(
                            coinsettings=message_coins,
                            region=user.get_coinsettings_region(),
                        )
                        if message_coins_for_region.count():
                            message_coins = message_coins_for_region.first()
                        user.deductCoins(
                            coins.coins_needed - message_coins.coins_needed, "IMAGE"
                        )
                        user.save()
            else:
                pass
            # Getting the current instance object to display in the template
            form.save()
            img_object = form.instance
            if file:
                file.close()

            return JsonResponse(
                {"img": str(img_object.image.url), "success": True}, safe=False
            )
        else:
            return JsonResponse({"success": False, "message": form.errors}, safe=False)

    return JsonResponse({"success": False, "message": "No Post"}, safe=False)


def update_email_settings(host, port, username, password, use_tls):
    """
    Update the email settings dynamically.
    """

    # Update the email settings variables
    settings.EMAIL_HOST = host
    settings.EMAIL_PORT = port
    settings.EMAIL_HOST_USER = username
    settings.EMAIL_HOST_PASSWORD = password
    settings.EMAIL_USE_TLS = use_tls


@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        email_object = EmailSettings.objects.first()
        sender = None
        if email_object:
            update_email_settings(
                host=email_object.email_host,
                port=email_object.email_port,
                username=email_object.email_host_user,
                password=email_object.email_host_password,
                use_tls=email_object.email_use_tls,
            )
            sender = email_object.default_from_email
        else:
            print("Email settings not found using default settings")
            sender = settings.DEFAULT_FROM_EMAIL
        try:
            data = json.loads(request.body)
            name = data['name']
            email = data['email']
            message = data['message']
            if name and email and message:
                contact_us = ContactUs(name=name, email=email, message=message)
                contact_us.save()
            try:
                send_mail(
                    'Contact Request Received',  # subject of the email
                    'We have received your contact request our team will contact you shortly.',  # message body
                    sender,  # sender email address
                    [email],  # recipient email addresses
                    fail_silently=False,  # raise an exception if sending fails
                )
                send_mail(
                    'Contact Request Received',  # subject of the email
                    # message body
                    f"you have received a contact request from user with {name} and email {email}. The message from user is '{message}'",
                    sender,  # sender email address
                    # recipient email addresses
                    ['contact-dev-testing@i69app.com'],
                    fail_silently=False,  # raise an exception if sending fails
                )
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
            return JsonResponse({'success': True})
        except (ValueError, KeyError):
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})
