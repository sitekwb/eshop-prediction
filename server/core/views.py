from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Conversion


def get_model_id(user_id):
    return user_id % 2

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



class PredictionView(APIView):
    pass