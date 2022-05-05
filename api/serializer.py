from rest_framework import serializers
from api.models import StationDatas

class StationdatasSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationDatas
        fields = "__all__"