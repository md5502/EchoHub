from django.shortcuts import get_object_or_404, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message, Music, Room, RoomMember
from .serializers import MessageSerializer, MusicSerializer, RoomDetailSerializer, RoomGetSerializer, RoomPostSerializer


class RoomApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        rooms_serialized_date = RoomGetSerializer(rooms, many=True)
        return Response(rooms_serialized_date.data)

    @swagger_auto_schema(request_body=RoomPostSerializer)
    def post(self, request):
        serializer = RoomPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RoomDetailApiView(APIView):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        room_serialized_date = RoomDetailSerializer(room)
        return Response(room_serialized_date.data)


class JoinRoomApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_pk):
        user = request.user
        room = get_object_or_404(Room, pk=room_pk)

        if RoomMember.objects.filter(room=room, user=user).exists():
            return Response({"msg": "You already joined the room"}, status=200)

        RoomMember.objects.create(room=room, user=user)
        return Response({"msg": "You have now joined the room"}, status=201)


class LeaveRoomApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_pk):
        user = request.user
        room = get_object_or_404(Room, pk=room_pk)
        room_member = RoomMember.objects.filter(room=room, user=user)

        if room_member.exists():
            room_member.delete()
            return Response({"msg": "You left the room"}, status=200)

        return Response({"msg": "You are not a member of this room"}, status=400)


class RoomMessagesApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_pk):
        room = get_object_or_404(Room, pk=room_pk)
        messages = room.room_messages.order_by("created_at")
        serialized_messages = MessageSerializer(messages, many=True)
        return Response(serialized_messages.data)

    @swagger_auto_schema(request_body=MessageSerializer)
    def post(self, request, room_pk):
        room = get_object_or_404(Room, pk=room_pk)
        user = request.user
        room_member = RoomMember.objects.filter(room=room, user=user).first()
        if not room_member:
            return Response({"msg": "You are not a member of this room"}, status=403)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=room, sender=room_member)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RoomMessagesDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, room_pk, message_pk):
        user = request.user
        room = get_object_or_404(Room, pk=room_pk)

        room_member = RoomMember.objects.filter(room=room, user=user).first()
        if not room_member:
            return Response({"msg": "You are not a member of this room"}, status=403)

        message = get_object_or_404(Message, pk=message_pk, room=room)
        if message.sender != room_member:
            return Response({"msg": "You are not allowed to delete this message"}, status=403)

        message.delete()
        return Response({"msg": "Message deleted successfully"}, status=204)


class MusicUploadApiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(request_body=MusicSerializer)
    def post(self, request):
        data = request.data.copy()
        data["uploaded_by"] = request.user.id

        serializer = MusicSerializer(data=data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicListApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        musics = Music.objects.all().order_by("-uploaded_at")
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)


class MusicDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        serializer = MusicSerializer(music)
        return Response(serializer.data)


class MusicDeleteApiView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        music = get_object_or_404(Music, pk=pk)
        if music.uploaded_by != request.user:
            return Response({"msg": "You are not allowed to delete this music."}, status=403)

        music.music_file.delete(save=False)
        music.delete()
        return Response({"msg": "Music deleted successfully."}, status=204)


def room_view(request, room_name):
    return render(request, "rooms/room.html", {"room_name": room_name})