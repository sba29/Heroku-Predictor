"""
Definition of views.
"""

from django.shortcuts import render
from app import generate_bracket
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import urllib
import boto3

listResults = []
listIndicator = []
listOrder = []

#scores_2013_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2013.txt"
#scores_2014_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2014.txt"
#scores_2015_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2015.txt"
#scores_2016_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2016.txt"
#scores_2017_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2017.txt"
#scores_2018_file = "https://s3.us-east-2.amazonaws.com/predictorbucket/static/app/content/Score_2018.txt"

#url2013 = urllib.urlopen(scores_2013_file)
#scores_13 = url2013.read().split()
#url2014 = urllib.urlopen(scores_2013_file)
#scores_14 = url2014.read().split()
#url2015 = urllib.urlopen(scores_2013_file)
#scores_15 = url2015.read().split()
#url2016 = urllib.urlopen(scores_2013_file)
#scores_16 = url2016.read().split()
#url2017 = urllib.urlopen(scores_2013_file)
#scores_17 = url2017.read().split()
#url2018 = urllib.urlopen(scores_2013_file)
#scores_18 = url2018.read().split()



def home(request): #home page request
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'html/index.html',
        {
        }
    )




def bracket(request): #bracket page request
    #inp_value = request.GET.getlist('selectInd', 'W')
    year_Val = request.GET.get('yearSelect','This is a default value')
    all_indicators = ['G','W','L','Eff','FGM','FG%','eFG%','FGA','FGM3','FG3%',
                      'FGA3','FTM','FT%','FTA','OR','ORB%','DR','DRB%','Ast','TO',
                      'TOV%','Stl','Blk','PF','OFGM','OFGA','OFG%','OeFG%','OFGM3',
                      'OFGA3','OFG3%','OFTM','OFTA','OFT%','OOR','OORB%','ODR',
                      'ODRB%','OAst','OTO','OTOV%','OStl','OBlk','OPF']
                
    # get checkbox values
    indicators = []
    weights = []
    for i in range(1, len(all_indicators)+1):
        indicator = request.GET.get('i' + str(i), 'off')
        if (indicator == 'on'):
            weight = int(request.GET.get('w' + str(i)))
            weights.append(weight)
            indicators.append(all_indicators[i - 1])
    year = int(year_Val)

    listResults = generate_bracket.get_tourney_results(year, indicators, weights)
    listOrder = generate_bracket.get_tourney_order(year)

    actual_results = generate_bracket.get_actual_results(year)
    points = generate_bracket.get_points(listResults, actual_results)
    percentage = points[1] * 100 / 63
    if listResults[5][0] == listResults[4][1]:
        loser = listResults[4][0]
        actual_loser = actual_results[4][0]
    else:
        loser = listResults[4][1]
        actual_loser = actual_results[4][1]
    green = "#008000"
    red = "#ff0000"
    colors = []

    for i in range(len(actual_results)):
        for j in range(len(actual_results[i])):
            if actual_results[i][j] == listResults[i][j] :
                colors.append(green)
            else:
                colors.append(red)
    if actual_loser == loser:
        colors.append(green)
    else:
        colors.append(red)

    results_with_names = []
    order_with_name = []


 #   for i in 'scores_' + str(year_Val):
 #       if points > i[0]:
 #           i=[points, indicators, weights]
 #           s3 = boto3.resource('s3')
 #           bucket = 'predictorbucket' 
 #           file_name = "static/app/content/Score_" + year_Val + ".txt"
 #           object = s3.Object(bucket, file_name)
 #           object.put(Body='scores_' + str(year_Val))
 #           break

        
    return render(
        request,
        'html/bracket.html',
        {
            'round1':order_with_name,
            'roundOthers':result,
            'loser':loser,
            'points':points[0],
            'games_correct':points[1],
            'percent_right':percentage,
            'colors':colors
        }
    )


# def bracket(request):
#    listResults = generateBracket.get_tourney_results(2015, ['OPF'])
#    listOrder = generateBracket.get_tourney_order(2015)
#    """Renders the home page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'html/bracket.html',
#        {
#            'round1':listOrder,
#            'roundOthers':listResults
#
#        }
