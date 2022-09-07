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
import json
# Create your views here.


class LeagueView(APIView):

    serializer_class = LeagueSerializer

    def get(self, request):
        league = [{'host': league.host, 'year_started': league.year_started, 'Espn_League_Id': league.Espn_League_Id, 'Espn_S2': league.Espn_S2, 'Espn_Swid': league.Espn_Swid, 'bigdata': league.bigdata}
        for league in League_Mod.objects.all()]
        return Response(league)

    def post(self, request):

        print(self.request.user)

        instanceOwners = []
        year = int(request.data['year_started'])
        print(year)
        currentOwners = []
        Owners = {

        }
        yearStandings = {

        }
        ##### Dicitonaries of Total Wins By Week #######

        # Loop One
        while year < 2022:
            league = League(league_id=request.data['Espn_League_Id'], year=year,
                            espn_s2=request.data['Espn_S2'], swid=request.data['Espn_Swid'])
            teams = league.teams

            # Creates the structure for my standings
            yearStandings.update({year: []})

            # Creates list of every owner
            for team in teams:

                # Sets wins and losses in the standings year arrays.
                yearStandings[year].append({
                    'owner': team.owner,
                    'wins': team.wins,
                    'losses': team.losses
                })
                if re.sub(' +', ' ', team.owner) not in instanceOwners:
                    instanceOwners.append(re.sub(' +', ' ', team.owner))
            print(year)
            year += 1
        year = int(request.data['year_started'])
        # declare another variable instead of still using the same "year"; its confusing for someone else look at code. Doesn't seem clean to increment a variable that has been assigned a payload.

        # Loop Two
        while year < 2022:
            league = League(league_id=request.data['Espn_League_Id'], year=year,
                            espn_s2=request.data['Espn_S2'], swid=request.data['Espn_Swid'])
            team_count = league.settings.team_count

            # Gets how many teams make playoffs in league
            playoff_team_count = league.settings.playoff_team_count
            teams = league.teams

            # This loop starts the bigdata process
            for owner in instanceOwners:
                # if this owner hasn't been created yet, it set the structure for their dict, and set all values to 0. This makese sure that at first year of league all current and future owners are accounted for.
                if owner not in Owners:
                    Owners[re.sub(' +', ' ', owner)] = {'name': owner, 'yearsPlayed': 0, 'count': 0, 'champ': 0,
                                  'finals': 0, 'madePlayoffs': 0, 'points_for': 0, 'points_against': 0, 'legacypoints': 0, year: []}
                    # loops through each team that is in league this year and get data neccessary for Legacy Points
                    for team in teams:
                        if(re.sub(' +', ' ', team.owner) == owner):
                            Owners[re.sub(' +', ' ', owner)
                                   ]['points_for'] += team.points_for
                            Owners[re.sub(' +', ' ', owner)
                                   ]['points_against'] += team.points_against
                            Owners[re.sub(' +', ' ', owner)
                                   ]['yearsPlayed'] += 1
                            if(team.final_standing == 1):
                                Owners[re.sub(' +', ' ', owner)]['champ'] += 1
                                Owners[re.sub(' +', ' ', owner)]['finals'] += 1
                            if(team.final_standing == 2):
                                Owners[re.sub(' +', ' ', owner)]['finals'] += 1
                            if(team.standing <= playoff_team_count):
                                Owners[re.sub(' +', ' ', owner)
                                       ]['madePlayoffs'] += 1

                # If the owner does exists, it updates their cumulative stats. and updates the year array.
                else:
                    for team in teams:
                        if(re.sub(' +', ' ', team.owner) == owner):
                            Owners[re.sub(' +', ' ', owner)
                                   ]['points_for'] += team.points_for
                            Owners[re.sub(' +', ' ', owner)
                                   ]['points_against'] += team.points_against
                            Owners[re.sub(' +', ' ', owner)
                                   ]['yearsPlayed'] += 1
                            if(team.final_standing == 1):
                                Owners[re.sub(' +', ' ', owner)]['champ'] += 1
                                Owners[re.sub(' +', ' ', owner)]['finals'] += 1
                            if(team.final_standing == 2):
                                Owners[re.sub(' +', ' ', owner)]['finals'] += 1
                            if(team.standing <= playoff_team_count):
                                Owners[re.sub(' +', ' ', owner)
                                       ]['madePlayoffs'] += 1
                    Owners[re.sub(' +', ' ', owner)].update({year: []})
            year += 1
        year = int(request.data['year_started'])

        # Loop 3
        while year < 2022:
            print(year)
            league = League(league_id=request.data['Espn_League_Id'], year=year,
                            espn_s2=request.data['Espn_S2'], swid=request.data['Espn_Swid'])

            teams = league.teams
            for team in teams:
                currentOwners.append(re.sub(' +', ' ', team.owner))

            weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

            for week in weeks:
                matchups = league.scoreboard(week)
                # Determines if owner won or lost each week that played.
                for matchup in matchups:
                    if matchup.home_score > matchup.away_score:
                        Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] = Owners[re.sub(
                            ' +', ' ', matchup.home_team.owner)]['count'] + 1
                        Owners[re.sub(' +', ' ', matchup.home_team.owner)][year].append(
                            Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'])
                        # checks to see if their is not an away team, aka league has a bye week.
                        if not matchup.away_team:
                            Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] = Owners[re.sub(
                                ' +', ' ', matchup.home_team.owner)]['count']
                        else:
                            Owners[re.sub(' +', ' ', matchup.away_team.owner)][year].append(
                                Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'])
                    elif matchup.away_score > matchup.home_score:
                        Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'] = Owners[re.sub(
                            ' +', ' ', matchup.away_team.owner)]['count'] + 1
                        Owners[re.sub(' +', ' ', matchup.away_team.owner)][year].append(
                            Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'])
                        Owners[re.sub(' +', ' ', matchup.home_team.owner)][year].append(
                            Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'])
                    else:
                        Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] = Owners[re.sub(
                            ' +', ' ', matchup.home_team.owner)]['count']

                for owner in instanceOwners:
                    if owner not in currentOwners:
                        Owners[owner][year].append(Owners[owner]['count'])

            currentOwners = []
            year += 1
        # Calculates Legacy Points
        for Owner in Owners:
            print(Owner)
            legacypoints = ((Owners[Owner]['count'] * 3) + (Owners[Owner]['champ'] * 70) + (Owners[Owner]
                            ['finals'] * 25) + (Owners[Owner]['madePlayoffs'] * 10) + (Owners[Owner]['points_for'] * .01))
            Owners[Owner]['legacypoints'] = legacypoints

        # save data to a serializable dictionary
        league_data = {
            'user': request.data['user'],
            'host': request.data['host'],
            'year_started': request.data['year_started'],
            'Espn_League_Id': request.data['Espn_League_Id'],
            'Espn_S2': request.data['Espn_S2'],
            'Espn_Swid': request.data['Espn_Swid'],
            'bigdata': Owners,
            'standings': yearStandings
        }
        serializer = LeagueSerializer(data=league_data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class LeagueDetail(APIView):

    def get_object(self, espn_league_id):
        try:
            return League_Mod.objects.get(Espn_League_Id=espn_league_id)
        except League_Mod.DoesNotExist:
            raise Http404

    # GETS LEAGUE DATA AND MANIPULATES IT TO BE CHART READY FOR WINS
    def get(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)

        Owners = League_Mod.objects.get(Espn_League_Id=espn_league_id).bigdata
        Chartdata = []
        # print(Owners['Jordan Freundlich'][startyear])

        for owner in Owners:
            #     # print(type(owner))
            #
            startyearget = League_Mod.objects.get(
                Espn_League_Id=espn_league_id).year_started
            startyearint = int(startyearget)
            startyearstr = str(startyearget)
            wins = []

            while startyearint < 2022:
                # print(startyearint)

                # creates one long array of wins for each owner
                for item in Owners[owner][str(startyearint)]:
                    wins.append(item)
                print(startyearint)
                startyearint += 1
            print(wins)

            # dictionary in the format canvas J.S needs it
            ownerdic = {
                'type': "spline",
                'visible': True,
                'showInLegend': True,
                'yValueFormatString': "## wins",
                'name': owner,
                'dataPoints': []
            }

            # loops through each item in the owners wins list and turns it into a Seperate dictionary, of label and y.
            week = 0
            yearget = League_Mod.objects.get(
                Espn_League_Id=espn_league_id).year_started
            yearint = int(yearget)
            for win in wins:
                week += 1
                if week == 17:
                    week = 1
                    yearint += 1
                dic = {
                    'label': f"{yearint} Week {week}",
                    'y': win
                }
                ownerdic['dataPoints'].append(dic)
            Chartdata.append(ownerdic)
        # print(Chartdata)

        # Serializabe dictionary
        leagueDetail = {
            'user': League_Mod.objects.get(Espn_League_Id=espn_league_id).user,
            'host': League_Mod.objects.get(Espn_League_Id=espn_league_id).host,
            'Espn_S2': League_Mod.objects.get(Espn_League_Id=espn_league_id).Espn_S2,
            'Espn_Swid': League_Mod.objects.get(Espn_League_Id=espn_league_id).Espn_Swid,
            'year_started': League_Mod.objects.get(Espn_League_Id=espn_league_id).year_started,
            'Espn_League_Id': League_Mod.objects.get(Espn_League_Id=espn_league_id).Espn_League_Id,
            'bigdata': Chartdata
        }

        print(leagueDetail)

        serializer = LeagueSerializer(leagueDetail)
        return Response(serializer.data)

    def put(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)
        serializer = LeagueSerializer(league, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        

    def delete(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)
        league.delete()
        return Response('league is deleted')

class BarChart(APIView):

    def get_object(self, espn_league_id):
        try:
            return League_Mod.objects.get(Espn_League_Id=espn_league_id)
        except League_Mod.DoesNotExist:
            raise Http404

     # GETS LEAGUE DATA AND MANIPULATES IT TO BE CHART READY FOR points barchart
    def get(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)

        Owners = League_Mod.objects.get(Espn_League_Id=espn_league_id).bigdata
        Chartdata = []
        # print(Owners['Jordan Freundlich'][startyear])

        for owner in Owners:
            #     # print(type(owner))
            #
            ownerdic = {
                'label': Owners[owner]['name'],
                'y': Owners[owner]['points_for']
            }

            Chartdata.append(ownerdic)
        # print(Chartdata)

        leagueDetail = {
            'user': League_Mod.objects.get(Espn_League_Id=espn_league_id).user,
            'host': League_Mod.objects.get(Espn_League_Id=espn_league_id).host,
            'Espn_S2': League_Mod.objects.get(Espn_League_Id=espn_league_id).Espn_S2,
            'Espn_Swid': League_Mod.objects.get(Espn_League_Id=espn_league_id).Espn_Swid,
            'year_started': League_Mod.objects.get(Espn_League_Id=espn_league_id).year_started,
            'Espn_League_Id': League_Mod.objects.get(Espn_League_Id=espn_league_id).Espn_League_Id,
            'bigdata': Chartdata
        }
        print(leagueDetail)
        serializer = LeagueSerializer(leagueDetail)
        return Response(serializer.data)

class LeagueDetailByIDView(APIView):
    def get_object(self, espn_league_id):
        # Returns an object instance that should
        # be used for detail views.
        try:
            return League_Mod.objects.get(Espn_League_Id=espn_league_id)
        except League_Mod.DoesNotExist:
            raise Http404

    # THIS IS THE MAIN GET FUNCTION OF DASHBOARD. GETS AND RETURNS ALL DATA
    def get(self, request, espn_league_id, format=None):
        league = self.get_object(espn_league_id)
        serializer = LeagueSerializer(league)
        return Response(serializer.data)


class UserLeagueByIDView(APIView):

    serializer_class = UserLeagueSerializer

    # Gets all the leagues. 
    def get(self, request):
        # userleague = [{'user': userleague.user, 'league': userleague.league}
        # for userleague in User_Leagues.objects.all()]
        # return Response(userleague)

        data = User_Leagues.objects.filter().values_list()
        responseData = list(data)
        return Response(responseData)
    #Creates a new league in user league lists. 
    def post(self, request):
        serializer = UserLeagueSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class NewCreateLeagueView(APIView):

    serializer_class = LeagueSerializer

    def get(self, request):
        league = [{'host': league.host, 'year_started': league.year_started, 'Espn_League_Id': league.Espn_League_Id, 'Espn_S2': league.Espn_S2, 'Espn_Swid': league.Espn_Swid, 'bigdata': league.bigdata}
        for league in League_Mod.objects.all()]
        return Response(league)

    # This creates the architecture for the league model. 
    def post(self, request):

        print(self.request.user)

        instanceOwners = []
        year = int(request.data['year_started'])
        print(year)
        currentOwners = []
        Owners = {

        }
        yearStandings = {

        }
        ##### Dicitonaries of Total Wins By Week #######

        # Loop One
        while year < 2022:
            league = League(league_id=request.data['Espn_League_Id'], year=year,espn_s2=request.data['Espn_S2'], swid=request.data['Espn_Swid'])
            teams = league.teams

            # Creates the structure for my strandings
            yearStandings.update({year: []})

            # Creates list of every owner
            for team in teams:

                # Sets wins and losses in the standings year arrays.
                yearStandings[year].append({
                    'owner': team.owner,
                    'wins': team.wins,
                    'losses': team.losses
                })
                if re.sub(' +', ' ', team.owner) not in instanceOwners:
                    instanceOwners.append(re.sub(' +', ' ', team.owner))
            print(year)
            year += 1
        print(instanceOwners)
        print(yearStandings)

        #Reset Year
        year = int(request.data['year_started'])

        #Loop 2
        while year < 2022:
            league = League(league_id=request.data['Espn_League_Id'], year=year,espn_s2=request.data['Espn_S2'], swid=request.data['Espn_Swid'])
            team_count = league.settings.team_count

            # Gets how many teams make playoffs in league
            playoff_team_count = league.settings.playoff_team_count
            teams = league.teams

            # This loop starts the bigdata process
            for owner in instanceOwners:
                # if this owner hasn't been created yet, it set the structure for their dict, and set all values to 0. This makese sure that at first year of league all current and future owners are accounted for.
                if owner not in Owners:
                    Owners[re.sub(' +', ' ', owner)] = {'name': owner, 'yearsPlayed': 0, 'count': 0, 'champ': 0,'finals': 0, 'madePlayoffs': 0, 'points_for': 0, 'points_against': 0, 'legacypoints': 0}
            print(year)
            year += 1
        year = int(request.data['year_started'])

        # save data to a serializable dictionary
        league_data = {
            'user': request.data['user'],
            'host': request.data['host'],
            'year_started': request.data['year_started'],
            'year': request.data['year_started'],
            'Espn_League_Id': request.data['Espn_League_Id'],
            'Espn_S2': request.data['Espn_S2'],
            'Espn_Swid': request.data['Espn_Swid'],
            'owners' : instanceOwners,
            'bigdata': Owners,
            'standings': yearStandings
        }
        serializer = LeagueSerializer(data=league_data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class NewCreateLeagueDetialView(APIView):
    serializer_class = LeagueSerializer

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

    # adds each input year to bigdata
    def put(self, request, espn_league_id, format=None):
        leagueModel = self.get_object(espn_league_id)

        currentOwners =[]
        print(request.data)
        standingsstr = request.data['standings']
        standings = request.data['standings']
        # standings = json.loads(standingsstr)
        Ownersstr = request.data['bigdata']
        Owners = request.data['bigdata']
        # Owners = json.loads(Ownersstr)
        instanceOwnersstr = request.data['owners']
        instanceOwners = request.data['owners']
        # instanceOwners = json.loads((instanceOwnersstr))
        year = int(request.data['year'])
        print(year)

        league = League(league_id=request.data['Espn_League_Id'], year=year,
                            espn_s2=request.data['Espn_S2'], swid=request.data['Espn_Swid'])
        team_count = league.settings.team_count
        # Gets how many teams make playoffs in league
        playoff_team_count = league.settings.playoff_team_count
        teams = league.teams
        # This loop starts the bigdata process
        for owner in instanceOwners:
            # print(owner)
            for team in teams:
                # print(team)
                if(re.sub(' +', ' ', team.owner) == owner):
                    Owners[re.sub(' +', ' ', owner)]['points_for'] += team.points_for
                    Owners[re.sub(' +', ' ', owner)]['points_against'] += team.points_against
                    Owners[re.sub(' +', ' ', owner)]['yearsPlayed'] += 1
                    if(team.final_standing == 1):
                        Owners[re.sub(' +', ' ', owner)]['champ'] += 1
                        Owners[re.sub(' +', ' ', owner)]['finals'] += 1
                    if(team.final_standing == 2):
                        Owners[re.sub(' +', ' ', owner)]['finals'] += 1
                    if(team.standing <= playoff_team_count):
                        Owners[re.sub(' +', ' ', owner)]['madePlayoffs'] += 1
            Owners[re.sub(' +', ' ', owner)].update({year: []})

        teams = league.teams
        for team in teams:
            currentOwners.append(re.sub(' +', ' ', team.owner))

        weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

        for week in weeks:
            matchups = league.scoreboard(week)
            # Determines if owner won or lost each week that played.
            for matchup in matchups:
                if matchup.home_score > matchup.away_score:
                    Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] = Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] + 1
                    Owners[re.sub(' +', ' ', matchup.home_team.owner)][year].append(Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'])
                    # checks to see if their is not an away team, aka league has a bye week.
                    if not matchup.away_team:
                        Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] = Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count']
                    else:
                        Owners[re.sub(' +', ' ', matchup.away_team.owner)][year].append(Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'])
                elif matchup.away_score > matchup.home_score:
                    Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'] = Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'] + 1
                    Owners[re.sub(' +', ' ', matchup.away_team.owner)][year].append(Owners[re.sub(' +', ' ', matchup.away_team.owner)]['count'])
                    Owners[re.sub(' +', ' ', matchup.home_team.owner)][year].append(Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'])
                else:
                    Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count'] = Owners[re.sub(' +', ' ', matchup.home_team.owner)]['count']
            for owner in instanceOwners:
                if owner not in currentOwners:
                    Owners[owner][year].append(Owners[owner]['count'])
        
        if year == 2021:
             # Calculates Legacy Points
            for Owner in Owners:
                print(Owner)
                legacypoints = ((Owners[Owner]['count'] * 3) + (Owners[Owner]['champ'] * 70) + (Owners[Owner]
                                ['finals'] * 25) + (Owners[Owner]['madePlayoffs'] * 10) + (Owners[Owner]['points_for'] * .01))
                Owners[Owner]['legacypoints'] = legacypoints

        print(Owners)
        league_data = {
            'user': request.data['user'],
            'host': request.data['host'],
            'year_started': request.data['year_started'],
            'year': request.data['year'],
            'Espn_League_Id': request.data['Espn_League_Id'],
            'Espn_S2': request.data['Espn_S2'],
            'Espn_Swid': request.data['Espn_Swid'],
            'bigdata': Owners,
            'standings': standings
        }

        # print(league_data)

        serializer = LeagueSerializer(leagueModel,data=league_data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# class MergeOwners(APIView):
#     serializer_class = MergeSerializer

#     def put(selfmrequest,espn_league_id, format = None):
#         league = self.get_object(espn_league_id)
#         print(request.data)
#         serializer = MergeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response('league was updated')


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
