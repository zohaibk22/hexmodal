import base64
from rest_framework import serializers
from .models import DeviceModel, PayloadModel

class PayloadSerializer(serializers.Serializer):
    fCnt = serializers.IntegerField()
    device = serializers.CharField(max_length=50)
    data_b64 = serializers.CharField(max_length=4096)
    rx_info = serializers.ListField(child=serializers.DictField(), required=False)
    tx_info = serializers.DictField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    def validate(self, attrs):
        b64 = attrs.get('data_b64')
        if not b64:
            raise serializers.ValidationError({"data_b64": "This field is required."})
        try:
            raw_data = base64.b64decode(b64, validate=True)
        except Exception as e:
            raise serializers.ValidationError({"data_b64": f"Invalid base64 string: {str(e)}"})
        data_hex = raw_data.hex()
        status = 'passing' if data_hex == '01' else 'failing'
        attrs['data_hex'] = data_hex
        attrs['status'] = status

        return attrs
    


    def create(self, validated_data):
        dev, _ = DeviceModel.objects.get_or_create(device_eui=validated_data['device'])
        validated_data.pop('device', None)
        payload = PayloadModel.objects.create(device=dev, **validated_data)
        dev.latest_status = payload.status
        dev.save(update_fields=['latest_status'])
        return payload

class PayloadResponseSerializer(serializers.ModelSerializer):
    devEUI = serializers.CharField(source='device.device_eui')
    class Meta:
        model = PayloadModel
        fields = ['fCnt', 'devEUI', 'data_b64', 'data_hex', 'status', 'rx_info', 'tx_info', 'created_at', 'updated_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = ['device_eui', 'latest_status']

   