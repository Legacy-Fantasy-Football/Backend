from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from espn_api.football import League
import re
# Create your views here.
  
class LeagueView(APIView):
    
    serializer_class = LeagueSerializer
  
    def get(self, request):
        league = [ {'code':league.code, 'host': league.host, 'Espn_League_Id': league.Espn_League_Id,'Espn_S2': league.Espn_S2,'Espn_Swid': league.Espn_Swid} 
        for league in League_Mod.objects.all()]
        return Response(league)
  
    def post(self, request):
        print(request.data['Espn_League_Id'])
        serializer = LeagueSerializer(data=request.data)

        instanceOwners=[]
        years= [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]

        currentOwners = []
        Owners = {

        }
        for year in years:
            league = League(league_id=request.data['Espn_League_Id'], year=year,espn_s2='AEAylLD7uSQQ7%2BenPr6av1H%2Fx0Hqbbpn8Jvr91ngxM1ll5ynO685mhN%2BSujz9I1IyJ6B1aZWsLiMmuPsdFk71SYQkvPUHFtQUQgN1rEs1mw%2FpRA8iI91nOAVwg1hfGb6TsZtvTJ9XHRr8C3E6uwLX4Yep2Pet%2FYN8%2BDm3QO8mSqXzfPkyS%2BsX50Mc5uvzCgV4r1pLIRXr%2FqnlfTiWHYCgZniEerPTLNhQaKqgaHAVPjCWUdZcPncMY6n9EX1eQnpB17eCXyP%2Fq4DXNNuRnASpnl%2ByoPm2%2Babp9yBTSJOy4N5zg%3D%3D', swid='{D19D67CA-C981-4CA2-8463-AF4111D2E8E2}')

            teams = league.teams

            # Creates list of every owner
            for team in teams:
                if re.sub(' +', ' ',team.owner) not in instanceOwners:
                        instanceOwners.append(re.sub(' +', ' ',team.owner))
            
            print(instanceOwners)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)

class LeagueDetail(APIView):
    def get_object(self, espn_league_id):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return League_Mod.objects.get(Espn_League_Id=espn_league_id)
        except League_Mod.DoesNotExist:
            raise Http404
  
    def get(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)
        serializer = LeagueSerializer(league)
        return Response(serializer.data)

    def put(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)
        serializer = LeagueSerializer(league, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response('league was updated')
  
    def delete(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)
        league.delete()
        return Response('league is deleted')
  

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/prediction/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)
