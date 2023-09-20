var notification_played = [false, false, false, false, false, false, false];

function notification_badge(data) {
    let count = [], list = [];
    let notification_name = ""
    let i;
    let message, item;

    for (i = 0; i < 7; i++) {
        count[i] = 0;
        list[i] = "";
    }

    for (i = 0; i < data.unread_list.length; i++) {
        item = data.unread_list[i];
        message = "";
        if (typeof item.verb !== 'undefined')
            message = item.verb;
        if (typeof item.timestamp !== 'undefined')
            message = message + " at " + item.timestamp;
        if (typeof item.description !== 'undefined')
            message = message + "<p class='dropdown-item-info'>[" + item.description + "]</p>";

        if (item.data['event_type'] == "COIN_PURCHASE") {
            count[0]++;
            list[0] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "coin_purchase";
        }
        else if (item.data['event_type'] == "PACKAGE_PURCHASE") {
            count[1]++;
            list[1] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "package_purchase";
        }
        else if (item.data['event_type'] == "GIFT_PURCHASE") {
            count[2]++;
            list[2] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "gift_purchase";
        }
        else if (item.data['event_type'] == "NEW_USER") {
            count[3]++;
            list[3] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "new_user";
        }
        else if (item.data['event_type'] == "REPORT_USER") {
            count[4]++;
            list[4] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "report_user";
        }
        else if (item.data['event_type'] == "REPORT_MOMENT" || item.data['event_type'] == "REPORT_STORY") {
            count[5]++;
            list[5] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "report_moment";
        }
        else if (item.data['event_type'] == "SERVER_ERROR") {
            count[6]++;
            list[6] += ("<li data-slug='" + item.slug + "'>" + message + "</li>");
            notification_name = "server_error";
        }
    }

    var notif_sound_type = 0;

    for (i = 1; i <= 7; i++) {
        if ($('#notify_list_' + i).css('display') == "none") {
            $('#badge_' + i).html(count[i - 1]);
            $('#notify_list_' + i).html(list[i - 1]);
            if (count[i - 1] == 0) { //no unread notification
                $('#badge_' + i).hide();
                notification_played[i - 1] = false;
            }
            else { // there is unread notification
                $('#badge_' + i).show();
                // select first unplayed notif sound
                if (notif_sound_type == 0 && !notification_played[i - 1])
                    notif_sound_type = i;
            }

            // handle extra icon of server error separately
            if (i == 7 && count[i - 1] == 0) {
                $('#badge_7_1').show();
                $('#notification_img_7').hide();
            }
            else {
                $('#badge_7_1').hide();
                $('#notification_img_7').show();
            }

        }
    }

    $.ajax({
        url: '/api/notificationsetting/sounds', success: function (data) {
            let sound_name = "";
            sound_name = data[notification_name];
            if (sound_name) play_notification(notif_sound_type, sound_name);
        }
    });

}

function show_notification_list(list_num) {
    var li_elem, i, slug, api_url;
    var list_id = '#notify_list_' + list_num;
    console.log("show_notification_list");
    if ($(list_id).css('display') != "none") {
        $(list_id).hide();
        $.ajax({ url: '/admin/admin-notifications/api/unread_list/?max=100', success: function (data) { notification_badge(data); } });
    }
    else if ($(list_id).html() != "") {
        $(list_id).show();

        li_elem = $(list_id).find('li');
        for (i = 0; i < li_elem.length; i++) {
            slug = $(li_elem[i]).data('slug');
            api_url = "/admin/admin-notifications/mark-as-read/" + slug;
            $.ajax({ url: api_url });
        }
    }

}

function play_notification(notif_sound_type, sound_name) {
    var base_url = "/media/";
    var file_url = base_url + sound_name;
    console.log(file_url);

    const audio = new Audio(file_url);
    const promise = audio.play();
    promise.then(() => {
        notification_played[notif_sound_type - 1] = true;
    }).catch(error => {
    });
}

