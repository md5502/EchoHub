from rest_framework import serializers

from .models import Message, Music, Room, RoomMember


class RoomGetSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Room
        fields = ["name", "discription", "is_private", "owner"]


class RoomPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomMemberSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = RoomMember
        fields = "__all__"


class RoomDetailSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    owner = serializers.CharField(source="owner.username", read_only=True)
    members = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_member_count(self, obj):
        return RoomMember.objects.filter(room=obj).count()

    def get_members(self, obj):
        members = RoomMember.objects.filter(room=obj)
        return RoomMemberSerializer(members, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MusicSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Music
        fields = "__all__"

    def validate_music_file(self, file):
        valid_mime_types = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp3"]
        valid_extensions = [".mp3", ".wav"]

        import mimetypes
        import os

        mime_type, _ = mimetypes.guess_type(file.name)
        ext = os.path.splitext(file.name)[1]  # noqa: PTH122, RUF100, W291

        if mime_type not in valid_mime_types or ext.lower() not in valid_extensions:
            raise serializers.ValidationError("Only MP3 and WAV files are allowed.")
        return file
