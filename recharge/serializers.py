from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import RechargeRecord


class RechargeRecordSerializer(ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = RechargeRecord
        fields = '__all__'
