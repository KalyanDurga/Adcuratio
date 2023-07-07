from app.models import *
from rest_framework import serializers


class TravelSeriallizer(serializers.ModelSerializer):
    class Meta:
        model=Travel
        fields=['name','description','place','state','state','images']