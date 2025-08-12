from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import PayloadSerializer, PayloadResponseSerializer, DeviceSerializer, DevicePayloadSerializer
from .models import DeviceModel, PayloadModel
from django.db.models import Prefetch


class IngestPayloadView(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes =  [IsAuthenticated]
    @transaction.atomic
    def post(self, request):

        payload_dict = {
            'device': request.data.get('devEUI'),
            'data_b64': request.data.get('data'),
            'fCnt': request.data.get('fCnt'),
            'rx_info': request.data.get('rxInfo', []),
            'tx_info': request.data.get('txInfo', {})
        }
        serialized_payload = PayloadSerializer(data=payload_dict)
        try:
            serialized_payload.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload_data = serialized_payload.save()
        
        except IntegrityError as e:
            return Response({"error": "Payload with this fCnt for the device already exists."}, status=status.HTTP_409_CONFLICT)
        
        return Response(PayloadResponseSerializer(payload_data).data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        payloads = PayloadModel.objects.all()
        serialized_payloads = PayloadResponseSerializer(payloads, many=True)
        return Response({'data': serialized_payloads.data}, status=status.HTTP_200_OK)



class DeviceView(APIView):
    def post(self, request):
        device_data = {
            'device_eui': request.data.get('devEUI', ''),
            'latest_status': request.data.get('status', 'unknown')
        }
        serialized_device = DeviceSerializer(data=device_data)
        try:
            serialized_device.is_valid(raise_exception=True)
            serialized_device.save()
            return Response({'message': 'Device created successfully', 'data': serialized_device.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Error occurred while creating new Device. Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        includes_payload = request.query_params.get('includes') == 'payloads'
    
        devices = DeviceModel.objects.all()
        if includes_payload:
            devices = devices.prefetch_related(Prefetch('payloads', queryset=PayloadModel.objects.order_by('-created_at')))
            serialized_devices = DevicePayloadSerializer(devices, many=True)
        else:
            serialized_devices = DeviceSerializer(devices, many=True)
        return Response({'data': serialized_devices.data}, status=status.HTTP_200_OK)
