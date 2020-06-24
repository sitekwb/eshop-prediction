import random

import pandas as pd
from core.models import Conversion
from keras.engine.saving import load_model
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import pickle
import os
from .apps import CoreConfig
import numpy as np

def get_model_id(user_id):
    return user_id % 2


def dummy_prediction(data):
    return [[np.random.uniform(0, 1)]]


def get_prediction_function(model_id):
    if model_id == 0:
        return dummy_prediction
    else:
        return CoreConfig.model.predict


def predict_lowest_effective_discount(data, prediction_function):
    max_indicator = 0
    final_discount = 0
    print(prediction_function.__name__)
    for discount in [0, 5, 10, 15, 20]:
        data_copy = data.copy()
        data_copy['discount'] = discount
        features = pd.DataFrame([data_copy])
        x = features
        # print('lista', x)

        x = CoreConfig.scaler.transform(x)
        # print('po skalowniu', x)
        prediction = prediction_function(x)
        current_prediction = prediction[0][0]
        current_indicator = current_prediction * (40 - discount)
        print(current_prediction)
        if max_indicator < current_indicator:
            max_indicator = current_indicator
            final_discount = discount
    return final_discount

class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Conversion


# noinspection PyAbstractClass
class UserIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


# noinspection PyMethodMayBeStatic
class ConversionView(APIView):
    """
    It accepts request like this:
    {
    "user_id" : 1234,
    "value" : 100
    }
    """
    def post(self, request, *args, **kwargs):
        user_serializer = UserIdSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        model_id = get_model_id(user_serializer.data['user_id'])
        data = {'value': request.data['value'], 'model_id': model_id}
        serializer = ConversionSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# noinspection PyAbstractClass
class PredictionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    price = serializers.FloatField()
    product_views_count = serializers.IntegerField()
    category_view_count = serializers.IntegerField()
    bought_with_lower_count = serializers.IntegerField()
    bought_category_count = serializers.IntegerField()
    time = serializers.FloatField()

    one_hot_city0 = serializers.IntegerField()
    one_hot_city1 = serializers.IntegerField()
    one_hot_city2 = serializers.IntegerField()
    one_hot_city3 = serializers.IntegerField()
    one_hot_city4 = serializers.IntegerField()
    one_hot_city5 = serializers.IntegerField()
    one_hot_city6 = serializers.IntegerField()
    one_hot_city7 = serializers.IntegerField()

    one_hot_category0 = serializers.IntegerField()
    one_hot_category1 = serializers.IntegerField()
    one_hot_category2 = serializers.IntegerField()
    one_hot_category3 = serializers.IntegerField()
    one_hot_category4 = serializers.IntegerField()
    one_hot_category5 = serializers.IntegerField()
    one_hot_category6 = serializers.IntegerField()
    one_hot_category7 = serializers.IntegerField()
    one_hot_category8 = serializers.IntegerField()
    one_hot_category9 = serializers.IntegerField()
    one_hot_category10 = serializers.IntegerField()
    one_hot_category11 = serializers.IntegerField()
    one_hot_category12 = serializers.IntegerField()
    one_hot_category13 = serializers.IntegerField()
    one_hot_category14 = serializers.IntegerField()


# noinspection PyMethodMayBeStatic
class PredictionView(APIView):
    """
    It accepts request like this:
    {"user_id": 1233, "price": 246.0, "product_views_count": 22, "category_view_count": 20, "bought_with_lower_count": 2, "bought_category_count": 3, "time": 1639.05, "one_hot_city0": 1, "one_hot_city1": 0, "one_hot_city2": 0, "one_hot_city3": 0, "one_hot_city4": 0, "one_hot_city5": 0, "one_hot_city6": 0, "one_hot_city7": 0, "one_hot_category0": 0, "one_hot_category1": 0, "one_hot_category2": 1, "one_hot_category3": 0, "one_hot_category4": 0, "one_hot_category5": 0, "one_hot_category6": 0, "one_hot_category7": 0, "one_hot_category8": 0, "one_hot_category9": 0, "one_hot_category10": 0, "one_hot_category11": 0, "one_hot_category12": 0, "one_hot_category13": 0, "one_hot_category14": 0}
    """

    def post(self, request, *args, **kwargs):
        prediction_serializer = PredictionSerializer(data=request.data)
        prediction_serializer.is_valid(raise_exception=True)

        model_id = get_model_id(prediction_serializer.data['user_id'])

        prediction_function = get_prediction_function(model_id)

        data = prediction_serializer.data
        del data['user_id']

        discount = predict_lowest_effective_discount(data, prediction_function)

        return Response({'discount': discount}, status=status.HTTP_201_CREATED)


class ResultsView(ListAPIView):
    queryset = Conversion.objects.all()
    serializer_class = ConversionSerializer


class ResetView(GenericAPIView):

    serializer_class = ConversionSerializer
    def post(self, request, *args, **kwargs):

        # list to force evaluation
        all_objects = list(Conversion.objects.all())
        count = len(all_objects)

        Conversion.objects.all().delete()

        serializer = self.get_serializer(all_objects, many=True)

        return Response({'deleted_count': count, 'deleted': serializer.data}, status=status.HTTP_200_OK)
