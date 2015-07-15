from django.shortcuts import render
from rest_framework import viewsets
from main.serializers import HeadShotsSerializer, TrialSerializer, UserSerializer
from main.models import HeadShots, Trial
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .permissions import IsStaffOrTargetUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     # allow non-authenticated user to create via POST
    #     return (AllowAny() if self.request.method == 'POST'
    #             else IsStaffOrTargetUser()),


class HeadShotsViewSet(viewsets.ViewSet):
    queryset = HeadShots.objects.all()

    def list(self, request):
        queryset = HeadShots.objects.all()
        serializer = HeadShotsSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        listOfThings = request.DATA['images']

        serializer = HeadShotsSerializer(
            data=listOfThings, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @detail_route(methods=['get'])
    def retrieve(self, request, pk=None):
        queryset = HeadShots.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        serializer = HeadShotsSerializer(image)
        return Response(serializer.data)

# class HeadShotsViewSet(viewsets.ModelViewSet):
#     queryset = HeadShots.objects.all()
#     serializer_class = HeadShotsSerializer


class TrialViewSet(viewsets.ViewSet):
    queryset = Trial.objects.all()

    def list(self, request):
        queryset = Trial.objects.all()
        serializer = TrialSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        listOfThings = request.DATA['names']

        serializer = TrialSerializer(
            data=listOfThings, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
