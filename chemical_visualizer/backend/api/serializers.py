from rest_framework import serializers
from .models import Dataset


class DatasetListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dataset
        fields = ("id", "name", "uploaded_at", "row_count", "summary")


class DatasetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dataset
        fields = (
            "id",
            "name",
            "uploaded_at",
            "row_count",
            "columns",
            "data",
            "summary",
        )
