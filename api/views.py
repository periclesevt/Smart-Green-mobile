from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import StationDatas
from api.serializer import StationdatasSerializer
from api.api import api

# Create your views here.

class StationDataViewSets(viewsets.ModelViewSet):
    queryset = StationDatas.objects.all()
    serializer_class = StationdatasSerializer
    api = api()

    @action(detail=True, methods=['POST'])
    def station_data(self, request, pk=None):
        body = request.data
        data = self.api.export(body.get('id', ''), body.get('data_init', ''), body.get('data_final', ''))

        return Response(data)
