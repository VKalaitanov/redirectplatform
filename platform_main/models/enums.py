from django.utils.translation import gettext_lazy as _
from django.db import models


class Geo(models.TextChoices):
    UK = 'uk', _("United Kingdom")
    US = 'us', _("United States")


class EmailType(models.TextChoices):
    NO_EMAIL = '0', _("No email")
    EMAIL = '1', _("Email")


class MobileOS(models.TextChoices):
    ANDROID = 'android', _("Android")
    IOS = 'ios', _("IOS")


class DesktopOS(models.TextChoices):
    WINDOWS = 'windows', _("Windows")
    LINUX = 'linux', _("Linux")
    MAC_OS = 'macos', _("MacOS")


class OperationalSystem(models.TextChoices):
    WINDOWS = 'windows', _("Windows")
    LINUX = 'linux', _("Linux")
    MAC_OS = 'macos', _("MacOS")
    ANDROID = 'android', _("Android")
    IOS = 'ios', _("IOS")


class Platform(models.TextChoices):
    DESKTOP = 'desktop', _("Desktop")
    MOBILE = 'mobile', _("Mobile")


class Format(models.TextChoices):
    POP = "pop", _("Pop")
    BANNER = "banner", _("Banner")
    REDIRECT = "redirect", _("Redirect")
