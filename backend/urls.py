"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('wel/', LeagueView.as_view(), name="something"),
    path('wins/<int:espn_league_id>/', LeagueDetail.as_view(), name="leagueDetail"),
    path('points/<int:espn_league_id>/', BarChart.as_view(), name="leagueDetail"),
    path('wel/<int:espn_league_id>/', LeagueDetailByIDView.as_view(), name="leagueDetail"),
    path('leagues/<int:user_id>/', UserLeagueByIDView.as_view(), name="userleagues"),
    # path('wel/<int:espn_league_id>/merge', MergeOwners.as_view(), name="leagueDetail"),
    path('api/', include("api.urls")),
]
