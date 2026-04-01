# Create your views here.
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.core.serializers import serialize
from .models import Point

def map_view(request):
    """Vue principale pour la carte"""
    # Récupérer les filtres depuis la requête
    filters = {}
    
    # Filtre par localité
    localite = request.GET.get('localite')
    if localite:
        filters['localite__icontains'] = localite
    
    # Filtre par altitude min/max
    altitude_min = request.GET.get('altitude_min')
    if altitude_min:
        filters['altitude__gte'] = altitude_min
    
    altitude_max = request.GET.get('altitude_max')
    if altitude_max:
        filters['altitude__lte'] = altitude_max
    
    # Filtre par ordre
    ordre = request.GET.get('ordre')
    if ordre:
        filters['ordre'] = ordre
    
    # Récupérer les points filtrés
    points = Point.objects.filter(**filters) if filters else Point.objects.all()
    
    # Convertir les points en GeoJSON
    points_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for point in points:
        feature = {
            "type": "Feature",
            "geometry": json.loads(point.geom.geojson),
            "properties": {
                "id": point.id_0,
                "nom": point.nom or "",
                "localite": point.localite or "",
                "altitude": float(point.altitude) if point.altitude else None,
                "est": float(point.est) if point.est else None,
                "nord": float(point.nord) if point.nord else None,
                "ordre": float(point.ordre) if point.ordre else None,
                "photo": point.photo or ""
            }
        }
        points_geojson["features"].append(feature)
    
    # Récupérer les valeurs uniques pour les filtres
    localites = Point.objects.values_list('localite', flat=True).distinct().exclude(localite__isnull=True).exclude(localite='')
    ordres = Point.objects.values_list('ordre', flat=True).distinct().exclude(ordre__isnull=True)
    
    context = {
        'points_geojson': json.dumps(points_geojson),
        'localites': sorted(list(set(localites))),
        'ordres': sorted(list(set(ordres))),
        'total_points': points.count(),
        'filters_applied': bool(filters)
    }
    
    return render(request, 'geodetic_app/map.html', context)

def get_points_api(request):
    """API pour récupérer les points en GeoJSON (pour AJAX)"""
    filters = {}
    
    # Appliquer les mêmes filtres que dans la vue principale
    localite = request.GET.get('localite')
    if localite:
        filters['localite__icontains'] = localite
    
    altitude_min = request.GET.get('altitude_min')
    if altitude_min:
        filters['altitude__gte'] = altitude_min
    
    altitude_max = request.GET.get('altitude_max')
    if altitude_max:
        filters['altitude__lte'] = altitude_max
    
    ordre = request.GET.get('ordre')
    if ordre:
        filters['ordre'] = ordre
    
    points = Point.objects.filter(**filters) if filters else Point.objects.all()
    
    # Utiliser le sérialiseur GeoDjango pour convertir en GeoJSON
    points_geojson = serialize('geojson', points, 
                               geometry_field='geom',
                               fields=('id_0', 'nom', 'localite', 'altitude', 'est', 'nord', 'ordre', 'photo'))
    
    return JsonResponse(json.loads(points_geojson), safe=False)