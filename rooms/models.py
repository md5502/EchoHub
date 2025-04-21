from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings import AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(_("name"), max_length=50)
    discription = models.TextField(_("discription"), blank=True, null=True)
    is_private = models.BooleanField(_("is private"), default=False)
    owner = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_("owner"), on_delete=models.CASCADE, related_name="Rooms")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    room_avatar = models.ImageField(_("room avatar"), upload_to="rooms/profiles", blank=True, null=True)

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    room = models.ForeignKey(Room, verbose_name=_("room"), on_delete=models.CASCADE, related_name="room_members")
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        related_name="joined_rooms",
    )
    joined_at = models.DateTimeField(_("joined at"), auto_now_add=True)
    is_muted = models.BooleanField(_("is muted"), default=False)
    is_admin = models.BooleanField(_("is admin"), default=False)

    def __str__(self):
        return self.room.name + "-" + self.user.username


class Message(models.Model):
    room = models.ForeignKey(Room, verbose_name=_("room"), on_delete=models.CASCADE, related_name="room_messages")
    sender = models.ForeignKey(RoomMember, verbose_name=_("sender"), on_delete=models.PROTECT)
    content = models.CharField(_("content"), max_length=2000)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("created at"), auto_now=True)

    def __str__(self):
        return self.content[:30]


class Music(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    music_file = models.FileField(_("File (optional)"), upload_to="rooms/musics")
    uploaded_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Uploaded By"),
        related_name="musics",
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="musics", verbose_name=_("Room"))
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.uploaded_by.username}"
