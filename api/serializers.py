from rest_framework import serializers

from .models import Data


class GenerateURLInputSerializer(serializers.Serializer):
    url = serializers.URLField()
    expire_days = serializers.IntegerField(min_value=1, max_value=365)


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'
        read_only_fields = ['id']

    def get_url(self):
        request = self.context.get('request')
        obj = self.instance
        if request:
            domain = request.build_absolute_uri('/')[:-1]
            return f"{domain}/{obj.code}"
        return obj.code
