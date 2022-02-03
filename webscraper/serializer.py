from rest_framework import serializers
from webscraper.models import StationDatas

class StationdatasSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationDatas
        fields = "__all__"