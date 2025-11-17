from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .serializers import DataSerializer, GenerateURLInputSerializer
from .models import Data


class GenerateURL(APIView):
    def get(self, request: Request):
        serializer = GenerateURLInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data['url']
        expire_days = serializer.validated_data['expire_days']

        instance = Data.objects.create(
            url=url,
            expire_days=expire_days
        )

        out = DataSerializer(instance, context={'request': request})

        return Response({
            'data': {
                'url': out.get_url(),
                'expire_days': expire_days
            },
            'error': None,
            'success': True
        }, status=status.HTTP_200_OK)


class GetURL(APIView):
    def get(self, request, code):
        try:
            data = Data.objects.get(code=code)

            if not data.is_expired():
                return redirect(data.url)
            else:
                return Response({
                    'data': None,
                    'error': {
                        'errorId': status.HTTP_410_GONE,
                        'isFriendly': True,
                        'errorMsg': "The entered code has expired."
                    },
                    'success': False
                }, status=status.HTTP_410_GONE)
        except Exception:
            return Response({
                'data': None,
                'error': {
                    'errorId': status.HTTP_404_NOT_FOUND,
                    'isFriendly': True,
                    'errorMsg': "The data in the entered code was not found."
                },
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)