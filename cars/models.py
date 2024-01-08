from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50)
    api_brand_id = models.CharField(max_length=50, null=True)
    icon = models.URLField(null=True, blank=True)
    used = models.PositiveIntegerField(default=0)
    top = models.BooleanField(default=False)
    cyrillic_name = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)

    class Meta:
        db_table = "brand"

    def __str__(self) -> str:
        return self.name
    

class CarModel(models.Model):
    name = models.CharField(max_length=50)
    api_model_id = models.CharField(max_length=70, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    used = models.PositiveIntegerField(default=0)
    cyrillic_name = models.CharField(max_length=50,null=True, blank=True)
    model_class = models.CharField(max_length=10, null=True, blank=True)
    year_from = models.SmallIntegerField(null=True, blank=True)
    year_to = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "car_model"

    def __str__(self) -> str:
        return self.name


class Generation(models.Model):
    api_generation_id = models.CharField(max_length=70, null=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    year_start = models.SmallIntegerField(null=True, blank=True)
    year_stop = models.SmallIntegerField(null=True, blank=True)
    isrestyle = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "generation"

    def __str__(self) -> str:
        return self.name
    

class Configuration(models.Model):
    api_configuration_id = models.CharField(max_length=50, null=True)
    generation = models.ForeignKey(Generation, on_delete=models.CASCADE)
    doors_count = models.SmallIntegerField(null=True, blank=True)
    body_type = models.CharField(max_length=60, null=True, blank=True)
    notice = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        db_table = "configuraton"

    def __str__(self) -> str:
        return self.api_configuration_id
    

class Modification(models.Model):
    api_modification_id = models.CharField(max_length=120, null=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE)
    offers_price_from = models.BigIntegerField(default=0, null=True)
    offers_price_to = models.BigIntegerField(default=0, null=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "modification"

    def __str__(self) -> str:
        return self.api_modification_id


class Specifications(models.Model):
    modification = models.OneToOneField(Modification, on_delete=models.CASCADE)
    horse_power = models.FloatField(null=True, blank=True)
    engine_type = models.CharField(max_length=100, null=True, blank=True)
    transmission = models.CharField(max_length=100, null=True, blank=True)
    drive = models.CharField(max_length=100, null=True, blank=True)
    volume = models.FloatField(default=0)
    time_to_100 = models.FloatField(default=0)
    max_speed = models.SmallIntegerField(default=0)
    diameter = models.FloatField(default=0)
    petrol_type = models.CharField(max_length=100, null=True, blank=True)
    weight = models.FloatField(default=0)
    height =  models.FloatField(default=0)
    width = models.FloatField(default=0)
    length = models.FloatField(default=0)
    fuel_tank_capacity = models.FloatField(default=0)
    volume_litres = models.FloatField(default=0)
    safety_rating = models.FloatField(default=0)
    safety_grade = models.FloatField(default=0)


    class Meta:
        db_table = "specifications"

    def __str__(self) -> str:
        return self.engine_type
    

class Options(models.Model):
    modification = models.OneToOneField(Modification, on_delete=models.CASCADE)
    electro_mirrors = models.BooleanField(default=True)
    airbag_side = models.BooleanField(default=True)
    hatch = models.BooleanField(default=True)
    led_light = models.BooleanField(default=True)
    rain_sensor = models.BooleanField(default=True)
    aux = models.BooleanField(default=True)

    class Meta:
        db_table = "options"


class Region(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "region"
    

class Car(models.Model):
    year = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    mileage = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "car"

    def __str__(self) -> str:
        return self.brand