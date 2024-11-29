from rest_framework import serializers

from .models import Station


class StationSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    technologies = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = [
            "id",
            "ne",
            "address",
            "latitude",
            "longitude",
            "gsm",
            "umts",
            "lte",
            "status",
            "status_display",  # Читаемый статус
            "technologies",  # Технологии станции
        ]
        read_only_fields = ["id", "status_display", "technologies"]

    def get_status_display(self, obj):
        """Возвращает текстовое представление статуса"""

        return "Активна" if obj.status else "Неактивна"

    def get_technologies(self, obj):
        """Возвращает список поддерживаемых технологий"""

        technologies = []
        if obj.gsm:
            technologies.append("GSM")
        if obj.umts:
            technologies.append("UMTS")
        if obj.lte:
            technologies.append("LTE")
        return ", ".join(technologies)

    def validate(self, data):
        """Валидация широты и долготы"""

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is not None and not (-90 <= latitude <= 90):
            raise serializers.ValidationError(
                {"latitude": "Широта должна быть в диапазоне от -90 до 90."}
            )
        if longitude is not None and not (-180 <= longitude <= 180):
            raise serializers.ValidationError(
                {"longitude": "Долгота должна быть в диапазоне от -180 до 180."}
            )

        return data
