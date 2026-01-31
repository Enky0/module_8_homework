from rest_framework import serializers


class YouTubeURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in value.lower() and 'youtu.be' not in value.lower():
            raise serializers.ValidationError("Ссылки должны быть только на YouTube")
        return value
