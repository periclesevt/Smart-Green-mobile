from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import StationDatas
from api.serializer import StationdatasSerializer
from .utils import parse_name
import requests

# Create your views here.
class StationDataViewSets(viewsets.ModelViewSet):
    #queryset = StationDatas.objects.all()
    #serializer_class = StationdatasSerializer

    @action(detail=True, methods=['POST'])
    def station_data(self, request, pk=None):
        body = request.data
        data = requests.get("https://apitempo.inmet.gov.br/estacao/{}/{}/{}"
            .format(
                body.get('data_init', ''),
                body.get('data_final', ''),
                body.get('id', '')
            )
        )

        # Extrai os valores da lista e adiciona a soma
        # ao objeto 'parsed_data'
        parsed_data = {}
        for row in data.json():
            for key,value in row.items():
                name = parse_name(key)
                
                if not name:
                    continue

                if name not in parsed_data:
                    parsed_data[name] = value
                elif type(value) in ['int', 'float']: 
                    parsed_data[name] += value

        # Tira a media dos valores brutos adicionados na etapa anterior
        for key, value in row.items():
            if type(value) in ['int', 'float']:
                row[key] = value/len(row.items())

        return Response({
            "message": "Average day data successfully getted",
            "data": parsed_data
        })
