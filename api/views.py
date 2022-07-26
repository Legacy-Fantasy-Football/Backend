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
        league = [ {'host': league.host, 'Espn_League_Id': league.Espn_League_Id,'Espn_S2': league.Espn_S2,'Espn_Swid': league.Espn_Swid, 'bigdata': league.bigdata} 
        for league in League_Mod.objects.all()]
        return Response(league)
  
    def post(self, request):

        instanceOwners=[]
        year = 2010
        currentOwners = []
        Owners = {

        }
        ##### Dicitonaries of Total Wins By Week #######
        while year < 2022:
            league = League(league_id=216415, year=year,espn_s2='AEAylLD7uSQQ7%2BenPr6av1H%2Fx0Hqbbpn8Jvr91ngxM1ll5ynO685mhN%2BSujz9I1IyJ6B1aZWsLiMmuPsdFk71SYQkvPUHFtQUQgN1rEs1mw%2FpRA8iI91nOAVwg1hfGb6TsZtvTJ9XHRr8C3E6uwLX4Yep2Pet%2FYN8%2BDm3QO8mSqXzfPkyS%2BsX50Mc5uvzCgV4r1pLIRXr%2FqnlfTiWHYCgZniEerPTLNhQaKqgaHAVPjCWUdZcPncMY6n9EX1eQnpB17eCXyP%2Fq4DXNNuRnASpnl%2ByoPm2%2Babp9yBTSJOy4N5zg%3D%3D', swid='{D19D67CA-C981-4CA2-8463-AF4111D2E8E2}')
            teams = league.teams
            # Creates list of every owner
            for team in teams:
                if re.sub(' +', ' ',team.owner) not in instanceOwners:
                        instanceOwners.append(re.sub(' +', ' ',team.owner))
            print(year)
            year += 1
        year=2010
        while year < 2022:
            league = League(league_id=216415, year=year,espn_s2='AEAylLD7uSQQ7%2BenPr6av1H%2Fx0Hqbbpn8Jvr91ngxM1ll5ynO685mhN%2BSujz9I1IyJ6B1aZWsLiMmuPsdFk71SYQkvPUHFtQUQgN1rEs1mw%2FpRA8iI91nOAVwg1hfGb6TsZtvTJ9XHRr8C3E6uwLX4Yep2Pet%2FYN8%2BDm3QO8mSqXzfPkyS%2BsX50Mc5uvzCgV4r1pLIRXr%2FqnlfTiWHYCgZniEerPTLNhQaKqgaHAVPjCWUdZcPncMY6n9EX1eQnpB17eCXyP%2Fq4DXNNuRnASpnl%2ByoPm2%2Babp9yBTSJOy4N5zg%3D%3D', swid='{D19D67CA-C981-4CA2-8463-AF4111D2E8E2}')

            teams = league.teams
            for team in teams:
                currentOwners.append(re.sub(' +', ' ',team.owner))

            for owner in instanceOwners:
                if owner not in Owners:
                    Owners[re.sub(' +', ' ',owner)] = {'count':0,year:[]}
                else:
                    Owners[re.sub(' +', ' ',owner)].update({year:[]})

            weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
                
            for week in weeks:
                matchups = league.scoreboard(week)

                for matchup in matchups:
                    if matchup.home_score > matchup.away_score:
                        Owners[re.sub(' +', ' ',matchup.home_team.owner)]['count'] = Owners[re.sub(' +', ' ',matchup.home_team.owner)]['count'] + 1
                        Owners[re.sub(' +', ' ',matchup.home_team.owner)][year].append(Owners[re.sub(' +', ' ',matchup.home_team.owner)]['count'])
                        Owners[re.sub(' +', ' ',matchup.away_team.owner)][year].append(Owners[re.sub(' +', ' ',matchup.away_team.owner)]['count'])
                    else:
                        Owners[re.sub(' +', ' ',matchup.away_team.owner)]['count'] = Owners[re.sub(' +', ' ',matchup.away_team.owner)]['count'] + 1
                        Owners[re.sub(' +', ' ',matchup.away_team.owner)][year].append(Owners[re.sub(' +', ' ',matchup.away_team.owner)]['count'])
                        Owners[re.sub(' +', ' ',matchup.home_team.owner)][year].append(Owners[re.sub(' +', ' ',matchup.home_team.owner)]['count'])
            
                for owner in instanceOwners:
                    if owner not in currentOwners:
                        Owners[owner][year].append(Owners[owner]['count']) 

            currentOwners = []
            year += 1

        Chartdata = []

        for owner in Owners:
            # wins = owners[owner][2010] + owners[owner][2011] + owners[owner][2012] + owners[owner][2013] + owners[owner][2014] + owners[owner][2015] + owners[owner][2016] + owners[owner][2017] + owners[owner][2018] + owners[owner][2019] + owners[owner][2020] + owners[owner][2021]
            startyear = 2010
            wins = []
            while startyear < 2022:
                for item in Owners[owner][startyear]:
                    wins.append(item)
                
                startyear += 1
            
            # print(wins)
            
            ownerdic = {
                'type': "spline",
                'visible': True,
                'showInLegend': True,
                'yValueFormatString': "## wins",
                'name': owner,
                'dataPoints': []
            }

            week = 0
            year = 2010
            for win in wins: 
                week+= 1
                if week == 17:
                    week = 1
                    year += 1
                dic = {
                    'label': f"{year} Week {week}",
                    'y': win
                }
                ownerdic['dataPoints'].append(dic)
            Chartdata.append(ownerdic)
        # print(data)

        league_data = {
            'host' : request.data['host'],
            'Espn_League_Id' :request.data['Espn_League_Id'],
            'Espn_S2' : request.data['Espn_S2'],
            'Espn_Swid' : request.data['Espn_Swid'],
            'bigdata' : Chartdata,
        }
        # request.data['BigData'] = Owners
        serializer = LeagueSerializer(data=league_data)
        print(serializer)
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
