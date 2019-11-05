from rest_framework.serializers import ModelSerializer,SlugRelatedField

from .models import OrderRecord


class OrderRecordSerializer(ModelSerializer):
    user = SlugRelatedField(read_only=True,slug_field='username')
    class Meta:
        model = OrderRecord
        fields = '__all__'