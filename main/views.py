from main.serializers import(
    HeadShotsSerializer,
    TrialSerializer,
    UserSerializer,
    ActorSerializer,
    ExperienceSerializer
)
from main import permissions as myPermissions
from main.models import HeadShots, Trial
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from main.models import Actor, Experience
from rest_framework import viewsets, permissions
from django.contrib.auth import authenticate, login


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    # allow non-authenticated user to create via POST
    #     return (permissions.AllowAny() if self.request.method == 'POST'
    #             else myPermissions.IsStaffOrTargetUser()),

    def perform_create(self, serializer):
        password = serializer.data['password']
        username = serializer.data['username']
        serializer.save()
        user = authenticate(
            username=username,
            password=password)
        login(self.request, user)


# class HeadShotsViewSet(viewsets.ViewSet):
#     queryset = HeadShots.objects.all()

#     def list(self, request):
#         queryset = HeadShots.objects.all()
#         serializer = HeadShotsSerializer(
#             queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def create(self, request):
#         listOfThings = request.DATA['images']

#         serializer = HeadShotsSerializer(
#             data=listOfThings, many=True)
#         if serializer.is_valid():
#             serializer.save(user_id=self.request.user.id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @detail_route(methods=['get'])
#     def retrieve(self, request, pk=None):
#         queryset = HeadShots.objects.all()
#         image = get_object_or_404(queryset, pk=pk)
#         serializer = HeadShotsSerializer(image)
#         return Response(serializer.data)

class HeadShotsViewSet(viewsets.ModelViewSet):
    queryset = HeadShots.objects.all()
    serializer_class = HeadShotsSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


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
            serializer.save(user_id=self.request.user.id)
            return Response(serializer.data)


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(id=self.request.user.id))
