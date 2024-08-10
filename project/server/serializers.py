from rest_framework import serializers
from server.models import Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    server_channels = ChannelSerializer(
        many=True,
        read_only=True,
    )
    count_members = serializers.IntegerField(
        read_only=True,
        source="num_members"
    )

    class Meta:
        model = Server
        exclude = ("members",)
