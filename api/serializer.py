from rest_framework import serializers
from . models import *
  
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['code','host', 'Espn_League_Id','Espn_S2','Espn_SWID']