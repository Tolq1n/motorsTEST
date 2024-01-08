from rest_framework.serializers import ModelSerializer
from .models import Car, Region, Brand, CarModel, Generation


class GenerationSerializer(ModelSerializer):
    class Meta:
        model = Generation
        fields = ['id', 'name', 'year_start', 'year_stop']


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'icon']


class CarModelSerializer(ModelSerializer):
    brand = BrandSerializer()
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'brand', 'year_from', 'year_to']

class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CarSerializer(ModelSerializer):
    car_model = CarModelSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'


class CarPostSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'