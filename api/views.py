from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *

# Create your views here.
  
class LeagueView(APIView):
    
    serializer_class = LeagueSerializer
  
    def get(self, request):
        league = [ {'code':league.code, 'host': league.host, 'Espn_League_Id': league.Espn_League_Id,'Espn_S2': league.Espn_S2,'Espn_SWID': Espn_SWID } 
        for league in League.objects.all()]
        return Response(league)
  
    def post(self, request):
  
        serializer = LeagueSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)