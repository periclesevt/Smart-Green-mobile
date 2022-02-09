from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from webscraper.models import StationDatas
from webscraper.serializer import StationdatasSerializer
from webscraper.webscraper import Webscraper

# Create your views here.

class StationDataViewSets(viewsets.ModelViewSet):
    queryset = StationDatas.objects.all()
    serializer_class = StationdatasSerializer
    webscraper = Webscraper()

    @action(detail=True, methods=['GET'])
    def station_data(self, request, pk=None):
        body = request.data
        data = self.webscraper.export(body.get('id', ''), body.get('data_init', ''), body.get('data_final', ''))

        return Response(data)
