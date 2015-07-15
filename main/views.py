from main.serializers import(
    HeadShotsSerializer,
    TrialSerializer,
    UserSerializer,
    ActorSerializer,
    ExperienceSerializer,
    RequestAccountNotificationSerializer
)
from main import permissions as myPermissions
from main.models import HeadShots, Trial
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from main.models import Actor, Experience, RequestAccountNotification
from rest_framework import viewsets, permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    # allow non-authenticated user to create via POST
    #     return (permissions.AllowAny() if self.request.method == 'POST'
    #             else myPermissions.IsStaffOrTargetUser()),


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


class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Actor.objects.all()
        elif self.request.user.is_authenticated():
            return Actor.objects.filter(
                id=Actor.objects.get(
                    user_id=self.request.user.id).id)
        else:
            return Actor.objects.none()


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(actor=Actor.objects.get(id=self.request.user.id))

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Experience.objects.all()
        elif self.request.user.is_authenticated():
            return Experience.objects.filter(
                actor_id=Actor.objects.get(
                    user_id=self.request.user.id))
        else:
            return Experience.objects.none()


class RequestAccountViewSet(viewsets.ModelViewSet):
    queryset = RequestAccountNotification.objects.all()
    serializer_class = RequestAccountNotificationSerializer
    permission_classes = (myPermissions.IsSuperUserOrTargetUser,)

    def get_queryset(self):
        if self.request.user and self.request.user.is_superuser:
            return RequestAccountNotification.objects.all()
        else:
            return RequestAccountNotification.objects.none()
