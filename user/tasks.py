import traceback
from datetime import timedelta

from celery import shared_task
from django.db.models import Count, Q
from django.utils import timezone

from chat.models import (
    DeletedMessage,
    DeletedMessageDate,
    Message,
    Notification,
    send_notification_fcm,
)
from user.models import ChatsQue, ChatsQueSetting, ModeratorOnlineScheduler, User

from .models import Settings
from .utils import notifiy_near_by_users


@shared_task(name="delete_old_deleted_messages")
def delete_old_deleted_messages(*args, **kwargs):
    no_of_days = DeletedMessageDate.objects.last().no_of_days
    DeletedMessage.objects.filter(
        deleted_timestamp__lte=timezone.now() - timedelta(days=7)
    )
    print(f"MESSAGE DELETED OLDER THAN {no_of_days} Days")


def _get_chat_queue_setting(task_name, default=1):
    try:
        setting = ChatsQueSetting.objects.filter(taskName=task_name).first()
        if not setting:
            return default
        time_map = {"Days": 86400, "Hours": 3600, "Minutes": 60, "Seconds": 1}
        value = setting.numberOfPeriods * time_map.get(setting.intervalPeriod)
        return value
    except Exception:
        return default


def _logout_worker(worker):
    try:
        user_token = None
        try:
            user_token = worker.auth_token
        except:
            print("No auth token")
        if user_token:
            try:
                worker.auth_token.delete()
                print("Logging out worker.")
            except:
                print("Token already deleted.")
        worker.isOnline = False
        worker.fake_users.clear()
        worker.save()
        print("Logging out worker with moderator user removed.")
    except Exception as e:
        print(e, "Failed to logout user")


@shared_task(name="chats_queue_scheduler_task")
def chats_queue_scheduler_task(*args, **kwargs):

    queue_chats = ChatsQue.objects.all().order_by("date_created")
    print(f"Chats in Queue {queue_chats.count()}")

    for chat in queue_chats:
        messages = Message.objects.filter(room_id=chat.room_id, restricted_msg=False).order_by("-timestamp")
        if not chat.isAssigned:
            for msg in messages:
                if msg.user_id.roles.filter(role__in=["MODERATOR"]):
                    break
                msg.read = None
                msg.save()

        if chat.isAssigned:
            if not chat.worker.isOnline:
                chat.moderator.owned_by.remove(chat.worker)
                chat.worker = None
                chat.isAssigned = False
                chat.save()

            time_from_db = _get_chat_queue_setting(
                task_name="unassign_chat_from_inactive_worker_to_active_worker_intervel",
                default=1,
            )

            unassigne_in_active_interval = timezone.now() - timezone.timedelta(
                seconds=time_from_db
            )

            print(f"Un Assigned Worker Time setting value {time_from_db} seconds")

            if chat.updated_at < unassigne_in_active_interval:
                available_workers = (
                    User.objects.filter(roles__role__in=["CHATTER"], isOnline=True)
                    .annotate(fake_count=Count("fake_users"))
                    .filter(fake_count__lt=1)
                )
                worker = None
                if available_workers.count() > 0:
                    worker = available_workers[0]
                if worker:
                    for msg in messages:
                        if msg.user_id.roles.filter(role__in=["MODERATOR"]):
                            break
                        msg.read = None
                        msg.save()
                    print(
                        "chat remove from worker and assign to other free online worker"
                    )
                    chat.moderator.owned_by.remove(chat.worker)
                    chat.moderator.owned_by.add(worker)
                    chat.worker = worker
                    chat.save()
                    print(f"assigning {chat.moderator} to ", worker)
                else:
                    print(f"Un Assigned Time is passed but no available worker")
                    chat.moderator.owned_by.remove(chat.worker)
                    chat.worker = None
                    chat.isAssigned = False
                    chat.save()
        else:
            available_workers = (
                User.objects.filter(roles__role__in=["CHATTER"], isOnline=True)
                .annotate(fake_count=Count("fake_users"))
                .filter(fake_count__lt=1)
            )

            if available_workers.count() > 0:
                chat.worker = available_workers[0]
                chat.isAssigned = True
                chat.save()
                available_workers[0].fake_users.add(chat.moderator)
                try:
                    last_message = Message.objects.filter(room_id__id=chat.room_id, restricted_msg=False).order_by("-timestamp").first()
                    if last_message:
                        last_message.receiver_worker = chat.worker
                        last_message.save()
                except:
                    pass
                print("chat assign to worker")

    logout_intervl_db = _get_chat_queue_setting(
        task_name="inactive_worker_logout_intervel", default=1
    )

    print(f"Logout In Active worker interval: {logout_intervl_db} seconds")

    online_workers = User.objects.filter(roles__role__in=["CHATTER"], isOnline=True)
    busy_workers = (
        User.objects.filter(roles__role__in=["CHATTER"], isOnline=True)
        .annotate(fake_count=Count("fake_users"))
        .filter(fake_count__gt=0)
    )
    print(f"Busy workers {busy_workers}")
    print(f"Online Workers: {online_workers}")

    for online_worker in online_workers:
        logout_intervl = timezone.now() - timezone.timedelta(seconds=logout_intervl_db)
        print(f"User Last seen {online_worker.user_last_seen} : Logout Date: {logout_intervl}")
        if online_worker.user_last_seen == None:
            _logout_worker(worker=online_worker)
        else:
            if online_worker.user_last_seen < logout_intervl:
                print("LoggingOut the Worker")
                _logout_worker(worker=online_worker)

    moderator_lists = ModeratorOnlineScheduler.objects.all()
    time = timezone.now().time()
    for list in moderator_lists:
        moderator_list = list.moderator_list.all()
        for moderator in moderator_list:
            if time > list.online_time and time < list.offline_time:
                if not moderator.isOnline:
                    moderator.isOnline = True
                    moderator.save()
            else:
                if moderator.isOnline:
                    moderator.isOnline = False
                    moderator.save()


@shared_task(name="unassign_moderator_from_inactive_workers")
def unassign_moderator_from_inactive_workers(*args, **kwargs):
    pass
    # time_before_6_minutes=timezone.now() - timezone.timedelta(minutes=6)
    # print(f" time befor 6 minutes {time_before_6_minutes}")
    # messages=Message.objects.filter(timestamp__lt=time_before_6_minutes,read=None,user_id__roles__role__in=['REGULAR']).filter(Q(room_id__user_id__roles__role__in=["MODERATOR"])|Q(room_id__target__roles__role__in=["MODERATOR"]))

    # rooms_id_list=set(messages.values_list("room_id",flat=True))

    # rooms=Room.objects.filter(id__in=rooms_id_list)

    # users=[]
    # for room in rooms:
    #     if room.user_id.roles.filter(role__in=['MODERATOR']):
    #         users.append(room.user_id)
    #     else:
    #         users.append(room.target)
    # available_workers=User.objects.filter(roles__role__in=['CHATTER'],isOnline = True).annotate(fake_count=Count("fake_users")).filter(fake_count__lt=1)

    # workers_with_5_moderators=[]
    # print(f"Moderators {users}")
    # while len(users):
    #     if list(available_workers)==workers_with_5_moderators:
    #         print("All workers are busy")
    #         break
    #     for worker in available_workers:
    #         if worker in workers_with_5_moderators:
    #             continue
    #         if worker.fake_users.all().count()<1:
    #             print(f"User {users[-1]}")
    #             old_worker=users[-1].owned_by.all()[0]
    #             if old_worker==worker:
    #                 continue

    #             moderator=users.pop()
    #             moderator.owned_by.remove(old_worker)
    #             moderator.owned_by.add(worker)
    #             print(f"moderator {moderator} removed from {old_worker} added to {worker}")

    #         else:
    #             print("{worker} worker is  busy")

    #             workers_with_5_moderators.append(worker)

    #         if len(users)==0:
    #             break

    # if users:
    #     for user in users:
    #         ModeratorQue.objects.get_or_create(moderator=user)
    #     print(f"{users} are the users added to uqueue.")

    # print(f"the users(moderators) who's owners has not taken action from last 6 minuts are {users}")


@shared_task(name="assign_moderator_from_inactive_to_active_workers")
def assign_moderator_from_inactive_to_active_workers(*args, **kwargs):
    pass
    # moderators = User.objects.filter(roles__role__in=['MODERATOR'])
    # print(moderators)
    # for moderator in moderators:
    #     print(moderator.owned_by.all())
    #     for worker in moderator.owned_by.all():
    #         if worker.isOnline:
    #             user_token=None
    #             try:
    #                 user_token=worker.auth_token
    #             except:
    #                 print("No auth token")

    #             if user_token:
    #                 now = timezone.now()
    #                 print("-------------",user_token.created)
    #                 print("Worker last seen was :", now - user_token.created)
    #                 moderator_logout_every_seconds = ModeratorQScheduler.objects.filter(taskName='moderator_logout_intervel')
    #                 second_interverl = 300
    #                 if moderator_logout_every_seconds.count()> 0:
    #                     second_interverl = moderator_logout_every_seconds[0].numberOfPeriods

    #                 print('second from db ',second_interverl)
    #                 if now > user_token.created + timezone.timedelta(
    #                         seconds=second_interverl):
    #                     # logout the worker
    #                     try:
    #                         worker.auth_token.delete()
    #                         worker.isOnline=False
    #                         worker.save()
    #                         print("Logging out worker.")
    #                     except:
    #                         print("Token already deleted.")

    #         else:
    #             ModeratorQue.objects.get_or_create(moderator=moderator)
    #             moderator.owned_by.remove(worker)

    # workers = User.objects.filter(roles__role__in=['CHATTER'],isOnline=True).annotate(fake_count=Count("fake_users")).filter(fake_count__lt=1)
    # print(workers)
    # for worker in workers:
    #     moderators = ModeratorQue.objects.filter(isAssigned=False)
    #     print(f"Moderator left in que {ModeratorQue.objects.filter(isAssigned=False).count()}")
    #     if moderators.count() > 0:
    #         topModeratorInQueue = ModeratorQue.objects.filter(isAssigned=False)[0]
    #         print('assign moderator to online worker')
    #         topModeratorInQueue.moderator.owned_by.add(worker)
    #         topModeratorInQueue.delete()

    # workers = User.objects.filter(roles__role__in=['CHATTER'])
    # for worker in workers:
    #     user_token=None
    #     try:
    #         user_token=worker.auth_token
    #     except:
    #         print("No auth token")

    #     if user_token:
    #         now = timezone.now()
    #         print("-------------",user_token.created)
    #         print("Worker last seen was :", now - user_token.created)
    #         if now > user_token.created + timezone.timedelta(
    #                 seconds=1800):
    #             # logout the worker
    #             try:
    #                 worker.auth_token.delete()
    #                 worker.isOnline=False
    #                 worker.save()
    #                 print("Logging out worker.")
    #             except:
    #                 print("Token already deleted.")

    #             current_moderators = worker.fake_users.all()
    #             if current_moderators.count() > 0:
    #                 for moderator in current_moderators:
    #                     old_owner = moderator.owned_by.all()[0]
    #                     moderator.owned_by.remove(old_owner)
    #                     push_moderator = ModeratorQue.objects.create(moderator=moderator)
    #                     print("Moderator added in que : ")
    #                     push_moderator.save()

    #     print("All moderators from inactive workers moved to que successfully.")

    # moderators = ModeratorQue.objects.filter(isAssigned=False)
    # if moderators.count() > 0:
    #     print("Assigning moderators to active workers : ")
    #     for worker in workers:
    #         print("checking for worker : ",worker.fullName)
    #         while (True):
    #             for moderator in moderators:
    #                 if worker.fake_users.count() < 1 and worker.isOnline:
    #                     x_moderator = User.objects.filter(id=moderator.moderator_id).first()
    #                     if x_moderator not in worker.fake_users.all():
    #                         if x_moderator.owned_by.all():
    #                             OLD=x_moderator.owned_by.all()[0]
    #                             x_moderator.owned_by.remove(OLD)
    #                             print(f"Assigned moderator {x_moderator.fullName} to worker {worker.fullName}")
    #                         else:
    #                             worker.fake_users.add(x_moderator)
    #                             moderator.delete()
    #                             print("RECORD DELETED FROM QUE....")
    #                 else:
    #                     print(f"Moderator left in que {ModeratorQue.objects.filter(isAssigned=False).count()}")
    #                     break
    #             break
    #     print(f"{ModeratorQue.objects.filter(isAssigned=False).count()} Moderators left in que.")


def recently_notified_user_ids():
    notification_setting = "MSGREMINDER"
    timedelta_10_min = timezone.now() - timezone.timedelta(minutes=10)
    notified_users = list(
        Notification.objects.select_related("user")
        .filter(
            created_date__gt=timedelta_10_min,
            notification_setting__id=notification_setting,
        )
        .distinct("user")
        .values_list("user__id", flat=True)
    )
    return notified_users


@shared_task(name="reminder_for_unread_messages")
def reminder_for_unread_messages(*args, **kwargs):
    messages = Message.objects.select_related("room_id").filter(read__isnull=True)
    already_notified_users = recently_notified_user_ids()
    # Calculate all unread messages for user from all the rooms
    for message in messages:
        room = message.room_id
        reciever = None
        if room.user_id == message.user_id:
            reciever = room.target
        else:
            reciever = room.user_id
        if reciever.id in already_notified_users:
            continue
        already_notified_users.append(reciever.id)
        unread_messasge_count = (
            Message.objects.filter(
                Q(Q(room_id__user_id=reciever) | Q(room_id__target_id=reciever))
                & Q(read__isnull=True)
            )
            .exclude(user_id=reciever)
            .count()
        )
        send_notification(reciever.id, unread_messasge_count)


def send_notification(user_id, unread_message_count):
    notification_setting = "MSGREMINDER"
    data = {
        "notification_type": notification_setting,
    }
    notification_obj = Notification(
        user_id=user_id,
        notification_setting_id=notification_setting,
        data=data
    )
    send_notification_fcm(
        notification_obj=notification_obj,
        message_count=f"You have {unread_message_count} unread messages",
    )


@shared_task(name="send_notification_to_nearby_users")
def send_notification_to_nearby_users(user_id):
    try:
        distance_km = Settings.get_setting(
            key="notify_new_user_radius_km", default=50000
        )
        notifiy_near_by_users(user_id=user_id, distance_km=distance_km)
    except Exception as e:
        print(traceback.print_exc(), e)
        print(f"Failed to send Notification")
