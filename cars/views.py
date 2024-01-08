from .models import *
from pprint import pprint
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import BrandSerializer, CarModelSerializer, RegionSerializer, CarSerializer, GenerationSerializer, CarPostSerializer


class ImagePostAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data['photos[]'])
        return Response({"Done"})


class GenerationListAPIVIew(APIView):
    def get(self, request, pk, *args, **kwargs):
        generations = Generation.objects.filter(car_model_id=pk)
        serialized = GenerationSerializer(generations, many=True)
        return Response(serialized.data)


class BrandListAPIView(ListAPIView):
    queryset = Brand.objects.exclude(used=0)
    serializer_class = BrandSerializer


class CarModelListAPIView(ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class ModelListAPIVIew(APIView):
    def get(self, request, pk, *args, **kwargs):
        models = CarModel.objects.filter(brand_id=pk)
        serialized = CarModelSerializer(models, many=True)
        return Response(serialized.data)


class FilteredCarsListAPIVIew(APIView):
    def get(self, request, pk, *args, **kwargs):
        cars = Car.objects.filter(car_model_id__generation__id=pk)
        serialized = CarSerializer(cars, many=True)
        return Response(serialized.data)
    

class CarCreateAPIView(CreateAPIView):
    serializer_class = CarPostSerializer
    queryset = Car.objects.all()
    

class DataMaker(APIView):
    def post(self, request, *args, **kwargs):
        url_mark_model = 'https://cars-base.ru/api/cars?full=1'
        response = requests.get(url_mark_model)

        # Check if the request was successful
        if response.status_code == 200:
            mark_models = response.json()  # Convert the response to JSON format
            pprint(type(mark_models))
            
            # cache = redis.Redis(host='localhost', port=6379, db=0)

            last_brand_id = Brand.objects.last().api_brand_id

            index = None

            for i, item in enumerate(mark_models):
                if item['id'] == last_brand_id:
                    index = i
                    break
            
            mark_models = mark_models[index+1:]

            for mark_model in mark_models:

                brand = Brand.objects.create(name=mark_model['name'], api_brand_id=mark_model['id'], top=mark_model['popular'], cyrillic_name=mark_model['cyrillic-name'], country=mark_model['country'])
                
                for model in mark_model['models']:

                    car_model = CarModel.objects.create(brand_id=brand.id, name=model['name'], api_model_id=model['id'], cyrillic_name=model['cyrillic-name'], model_class=model['class'], year_from=model['year-from'], year_to=model['year-to'])

                    url_model_generation=f"https://cars-base.ru/api/cars/{mark_model['id']}/{model['id']}?key=1f6e75680"

                    response_generations = requests.get(url_model_generation)

                    generations = response_generations.json()

                    for generation in generations:

                        model_generation = Generation.objects.create(car_model_id=car_model.id, api_generation_id=generation['id'], name=generation['name'], year_start=generation['year-start'], year_stop=generation['year-stop'], isrestyle=generation['is-restyle'])
                        
                        url_config_modific_speci_options=f"https://cars-base.ru/api/cars/{mark_model['id']}/{model['id']}/{generation['id']}?key=1f6e75680"

                        response_config_modific_speci_options = requests.get(url_config_modific_speci_options)

                        parametres = response_config_modific_speci_options.json()

                        for parameter in parametres:

                            config=Configuration.objects.create(api_configuration_id=parameter['id'], generation_id=model_generation.id, doors_count=parameter['doors-count'], body_type=parameter['body-type'], notice=parameter['notice'])

                            for modification in parameter['modifications']:

                                modif = Modification.objects.create(api_modification_id=modification['complectation-id'], configuration_id=config.id, offers_price_from=modification['offers-price-from'], offers_price_to=modification['offers-price-to'], group_name=modification['group-name'])

                                if 'specifications' in modification:

                                    horse_power = modification['specifications']['horse-power'] if 'horse-power' in modification['specifications'] else 0

                                    engine_type = modification['specifications']['engine-type'] if 'engine-type' in modification['specifications'] else 0

                                    transmission = modification['specifications']['transmission'] if 'transmission' in modification['specifications'] else None

                                    drive = modification['specifications']['drive'] if 'drive' in modification['specifications'] else None

                                    volume = modification['specifications']['volume'] if 'volume' in modification['specifications'] else 0

                                    time_to_100 = modification['specifications']['time-to-100'] if 'time-to-100' in modification['specifications'] else 0

                                    max_speed = modification['specifications']['max-speed'] if 'max-speed' in modification['specifications'] else 0

                                    diameter = modification['specifications']['diameter'] if 'diameter' in modification['specifications'] else 0

                                    petrol_type = modification['specifications']['petrol-type'] if 'petrol-type' in modification['specifications'] else None

                                    weight = modification['specifications']['weight'] if 'weight' in modification['specifications'] else 0

                                    height = modification['specifications']['height'] if 'height' in modification['specifications'] else 0

                                    width = modification['specifications']['width'] if 'width' in modification['specifications'] else 0

                                    length = modification['specifications']['length'] if 'length' in modification['specifications'] else 0


                                    fuel_tank_capacity = modification['specifications']['fuel-tank-capacity'] if 'fuel-tank-capacity' in modification['specifications'] else 0


                                    volume_litres = modification['specifications']['volume-litres'] if 'volume-litres' in modification['specifications'] else 0

                                    safety_rating = modification['specifications']['safety-rating'] if 'safety-rating' in modification['specifications'] and modification['specifications']['safety-rating'].isdigit() else 0

                                    safety_grade = modification['specifications']['safety-grade'] if 'safety-grade' in modification['specifications'] else 0
                                    
                                    Specifications.objects.create(modification_id=modif.id, horse_power=horse_power, engine_type=engine_type, \
                                                                transmission=transmission, drive=drive, volume=volume, \
                                                                    time_to_100=time_to_100, max_speed=max_speed, diameter=diameter, \
                                                                        petrol_type=petrol_type, weight=weight, height=height, \
                                                                            width=width, length=length, fuel_tank_capacity=fuel_tank_capacity, \
                                                                                volume_litres=volume_litres, safety_rating=safety_rating, safety_grade=safety_grade)
                                
                                if 'options' in modification:

                                    electro_mirrors = modification['options']['electro-mirrors'] if 'electro-mirrors' in modification['options'] and modification['options']['electro-mirrors'] is bool else 0

                                    airbag_side = modification['options']['airbag-side'] if 'airbag-side' in modification['options'] and modification['options']['airbag-side'] is bool else 0

                                    hatch = modification['options']['hatch'] if 'hatch' in modification['options'] and modification['options']['hatch'] is bool else 0

                                    led_light = modification['options']['led-light'] if 'led-light' in modification['options'] else 0

                                    rain_sensor = modification['options']['rain-sensor'] if 'rain-sensor' in modification['options'] else 0

                                    aux = modification['options']['aux'] if 'aux' in modification['options'] else 0

                                    try:
                                        Options.objects.create(modification_id=modif.id, electro_mirrors=electro_mirrors, airbag_side=airbag_side, hatch=hatch, led_light=led_light, rain_sensor=rain_sensor, aux=aux)
                                    except Exception as e:
                                        print(e)
                                        print('e mirrors', electro_mirrors, 'airbag side', airbag_side, 'hatch', hatch, 'led-light', led_light, 'rain-sensor', rain_sensor, 'aux', aux)

            return Response("All done")
        else:
            return Response({"error": "Failed to fetch data from the API."}, status=response.status_code)



