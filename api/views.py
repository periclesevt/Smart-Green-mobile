from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import StationDatas
from api.serializer import StationdatasSerializer
from .utils import parse_name,isnumber
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
        ).json()

        # Extrai os valores da lista e adiciona a soma
        # ao objeto 'parsed_data'
        field_count = {}
        parsed_data = {}
        for row in data:
            for key,value in row.items():
                name = parse_name(key)
                
                if not name:
                    continue
                if value is None:
                    continue
                if name == "Rn" and float(value) < 0:
                    continue

                if name not in parsed_data:
                    field_count[name] = 0
                    if isnumber(value):
                        parsed_data[name] = float(value)
                    else:
                        parsed_data[name] = value
                        
                elif isnumber(value):
                    parsed_data[name] += float(value)
                
                field_count[name] += 1

        # Tira a media dos valores brutos adicionados na etapa anterior
        #Rn KJm² --> MJm²d¹
        #P mB --> kPa (divisão por 10)  
        for key, value in parsed_data.items():
            if isinstance(value,float) and key != "Rn":
                print(field_count)
                parsed_data[key] = value/field_count[key]

        return Response({
            "message": "Average day data successfully getted",
            "data": parsed_data
        })

