from rest_framework.urls import path

from .views import (
    JoinRoomApiView,
    LeaveRoomApiView,
    MusicDeleteApiView,
    MusicDetailApiView,
    MusicListApiView,
    MusicUploadApiView,
    RoomApiView,
    RoomDetailApiView,
    RoomMessagesApiView,
    RoomMessagesDeleteApiView,
)

app_name = "Rooms"

urlpatterns = [
    path("", RoomApiView.as_view(), name="room_list"),
    path("<int:pk>", RoomDetailApiView.as_view(), name="room_detaile"),
    path("<int:room_pk>/join/", JoinRoomApiView.as_view(), name="room_join"),
    path("<int:room_pk>/leave/", LeaveRoomApiView.as_view(), name="room_leave"),
    path("<int:room_pk>/messages/", RoomMessagesApiView.as_view(), name="room_messages_list_create"),
    path("<int:room_pk>/messages/<int:message_pk>/", RoomMessagesDeleteApiView.as_view(), name="room_message_delete"),
    path("music/upload/", MusicUploadApiView.as_view(), name="music-upload"),
    path("music/", MusicListApiView.as_view(), name="music-list"),
    path("music/<int:pk>/", MusicDetailApiView.as_view(), name="music-detail"),
    path("music/<int:pk>/delete/", MusicDeleteApiView.as_view(), name="music-delete"),
]
