"""
Definition of views.
"""

from django.shortcuts import render
from app import generate_bracket
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
listResults = []
listIndicator = []
listOrder = []
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
    all_indicators = ['G','W','L','FGM','FGA','FG%','FGM3','FGA3','FG3%','FTM',
                      'FTA','FT%','OR','DR','Ast','TO','Stl','Blk','PF','OFGM',
                      'OFGA','OFGM3','OFGA3','OFTM','OFTA','OOR','ODR','OAst',
                      'OTO','OStl','OBlk','OPF']
    # get checkbox values
    indicators = []
    weights = []
    for i in range(1, 33):
        indicator = request.GET.get('i' + str(i), 'off')
        weight = int(request.GET.get('j' + str(i)))
        if (indicator == 'on'):
            weights.append(weight)
            indicators.append(all_indicators[i - 1])
    year = int(year_Val)

    listResults = generate_bracket.get_tourney_results(year, indicators, weights)
    listOrder = generate_bracket.get_tourney_order(year)

    actual_results = generate_bracket.get_actual_results(year)
    points = generate_bracket.get_points(listResults, actual_results)
    percentage = points[1] * 100 /63
    print(points[1])
    if listResults[5][0] == listResults[4][1]:
        loser = listResults[4][0]
    else:
        loser = listResults[4][1]

    return render(
        request,
        'html/bracket.html',
        {
            'round1':listOrder,
            'roundOthers':listResults,
            'loser':loser,
            'points':points[0],
            'game_correct':points[1],
            'percent_right':percentage
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
