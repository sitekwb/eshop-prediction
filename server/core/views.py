from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Conversion


# class ConversionSerializer(serializers.Serializer):
#     value = serializers.IntegerField()
#     model_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Conversion(**validated_data)
#

class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Conversion


# noinspection PyAbstractClass
class UserIdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


# noinspection PyMethodMayBeStatic
class ConversionView(APIView):

    def post(self, request, *args, **kwargs):
        UserIdSerializer(data=request.data).is_valid(raise_exception=True)

        model_id = request.data['user_id'] % 2
        data = {'value': request.data['value'], 'model_id': model_id}
        serializer = ConversionSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
