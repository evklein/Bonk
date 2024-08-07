from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Round, HoleStats, Stroke, Putt
from course.models import Course, Hole, Tee

def index(request):
    return HttpResponse("Hello, world. You're at the rounds index.")

def fetchRound(request, round_id):
    round = Round.objects.get(pk=round_id)
    raw_data = serializers.serialize('json', [round], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchRoundsInProgress(request):
    rounds = Round.objects.filter(in_progress=True).order_by('-date_played')
    raw_data = serializers.serialize('json', rounds)
    return HttpResponse(raw_data, content_type='application/json')

def fetchAllHoleStatsForRound(request, round_id):
    hole_scores = HoleStats.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', hole_scores)
    return HttpResponse(raw_data, content_type='application/json')

def fetchHoleStats(request, round_id, hole_id):
    hole_score = HoleStats.objects.filter(rnd=round_id, hole=hole_id).first()
    raw_data = serializers.serialize('json', [hole_score], ensure_ascii=False)
    trimmed_data = raw_data[1:-1]
    return HttpResponse(trimmed_data, content_type='application/json')

def fetchHoleStrokes(request, round_id, hole_id):
    strokes = Stroke.objects.filter(hole_score=hole_score_id)
    raw_data = serializers.serialize('json', strokes)
    return HttpResponse(raw_data, content_type='application/json')

def fetchHolePutts(request, round_id, hole_id):
    putts = Putt.objects.filter(hole_score=hole_score_id)
    raw_data = serializers.serialize('json', putts)
    return HttpResponse(raw_data, content_type='application/json')

def fetchRoundHoleStats(request, round_id):
    stats = HoleStats.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', stats)
    return HttpResponse(raw_data, content_type='application/json')

def fetchRoundStrokes(request, round_id):
    strokes = Stroke.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', strokes)
    return HttpResponse(raw_data, content_type='application/json')

def fetchRoundPutts(request, round_id):
    putts = Putt.objects.filter(rnd=round_id)
    raw_data = serializers.serialize('json', putts)
    return HttpResponse(raw_data, content_type='application/json')

@csrf_exempt
def saveNewRound(request):
    if request.method == 'POST':
        try:
            course_id = request.GET.get('course_id', -1)
            print("COURSE ID")
            print(course_id)
            course = Course.objects.get(pk=course_id)
            tee_id = request.GET.get('tee_id', -1)
            tee = Tee.objects.get(pk=tee_id)

            data = json.loads(request.body)
            round = Round(course=course, played_tee=tee)
            for key, value in data.items():
                setattr(round, key, value)
            round.in_progress = True
            
            round.save()

            return JsonResponse({'message': 'Data saved successfully', 'round_id': round.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def updateRound(request, round_id):
    if request.method == 'POST':
        try:
            round = Round.objects.get(pk=round_id)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(round, key, value)
            round.in_progress = True
            
            round.save()

            return JsonResponse({'message': 'Data saved successfully', 'round_id': round.id})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def saveHoleStats(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)
            
            stats, created = HoleStats.objects.update_or_create(
                rnd=rnd, 
                hole=hole, 
                defaults=data
            )
            return JsonResponse({'message': 'Data saved successfully', 'created': created})

            stats.save()

            return JsonResponse({'message': 'Data saved successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def saveStroke(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)

            stroke, created = Stroke.objects.update_or_create(
                rnd=rnd, 
                hole=hole, 
                stroke_number=data['stroke_number'],
                defaults=data
            )
            return JsonResponse({'message': 'Data saved successfully', 'created': created})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def savePutt(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            data = json.loads(request.body)

            putt, created = Putt.objects.update_or_create(
                rnd=rnd, 
                hole=hole, 
                stroke_number=data['stroke_number'],
                defaults=data
            )
            return JsonResponse({'message': 'Data saved successfully', 'created': created})

        except Round.DoesNotExist:
            return JsonResponse({'error': 'Round not found'}, status=404)
        except Hole.DoesNotExist:
            return JsonResponse({'error': 'Hole not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def purgeShots(request, round_id, hole_id):
    if request.method == 'POST':
        try:
            rnd = Round.objects.get(pk=round_id)
            hole = Hole.objects.get(pk=hole_id)
            putts = Putt.objects.filter(rnd=rnd, hole=hole)
            strokes = Stroke.objects.filter(rnd=rnd, hole=hole)

            putts.delete()
            strokes.delete()
            return JsonResponse({'message': 'Strokes and putts removed successfully'})
        except Round.DoesNotExist:
            return JsonResponse({'error': 'Round not found'}, status=404)
        except Hole.DoesNotExist:
            return JsonResponse({'error': 'Hole not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
