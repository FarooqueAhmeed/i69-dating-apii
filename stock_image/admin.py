from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django import forms
from django.forms.widgets import ClearableFileInput

# Register your models here.
from .models import StockImage

# Register your models here.
from .models import StockImage

# admin.site.register(StockImage)


class AdminImageWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                '<a href="%s" target="_blank">'
                '<img src="%s" alt="%s" style="max-width: 200px; max-height: 200px; border-radius: 5px;" />'
                "</a><br/><br/> " % (image_url, image_url, file_name)
            )
        output.append(super(ClearableFileInput,
                      self).render(name, value, attrs))
        return mark_safe("".join(output))


class StockImageAdminForm(forms.ModelForm):
    class Meta:
        model = StockImage
        fields = "__all__"
        widgets = {"file": AdminImageWidget}


@admin.register(StockImage)
class StockImageAdmin(admin.ModelAdmin):
    list_display = ("id", "view_thumbnail")
    form = StockImageAdminForm

    def view_thumbnail(self, obj):
        output = []
        if obj.file:
            image_url = obj.file.url
            output.append(
                '<a href="javascript:;" class="mtooltip left">'
                '<img src="%s" alt="" style="max-width: 100px; max-height: 100px;" />'
                '<span><img src="%s" style="max-width: 600px; max-height: 600px;"/></span>'
                "</a>" % (image_url, image_url)
            )

            style_css = """
            <style>
            a.mtooltip { outline: none; cursor: help; text-decoration: none; position: relative;}
            a.mtooltip span {margin-left: -999em; padding:5px 6px; position: absolute; width:auto; white-space:nowrap; line-height:1.5;box-shadow:0px 0px 10px #999; -moz-box-shadow:0px 0px 10px #999; -webkit-box-shadow:0px 0px 10px #999; border-radius:3px 3px 3px 3px; -moz-border-radius:3px; -webkit-border-radius:3px;}
            a.mtooltip span img {max-width:600px;}
            a.mtooltip {background:#ffffff; text-decoration:none;cursor: help;} /*BG color is a must for IE6*/
            a.mtooltip:hover span{ left: 1em;top: 0em; margin-left: 0; z-index:99999; position:absolute; background:#ffffff; border:1px solid #cccccc; color:#6c6c6c;}

            #changelist-form .results{overflow-x: initial!important;}
            </style>
            """
            output.append(style_css)
        return mark_safe("".join(output))

