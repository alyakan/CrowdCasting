
from main.models import (
    Actor,
    RequestContactInfo)
from rest_framework import viewsets, permissions
from rest_framework import serializers
from main.serializers import(
    UserSerializer,
    ActorSerializer,
    RequestContactInfoSerializer,

)
from main import permissions as myPermissions
# from rest_framework import status
# from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
<<<<<<< HEAD
from rest_framework.decorators import detail_route, list_route
from django.core.mail import EmailMultiAlternatives
=======
from django.http import JsonResponse
>>>>>>> b110d344bf5233274235347420541d9209765171


class index(TemplateView):
    template_name = "main/index.html"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (myPermissions.UserIsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    # def get_permissions(self):
    # allow non-authenticated user to create via POST
    #     return (permissions.AllowAny() if self.request.method == 'POST'
    #             else myPermissions.IsStaffOrTargetUser()),

    def perform_create(self, serializer):
        password = serializer.data['password']
        username = serializer.data['username']
        user = serializer.save()
        Actor.objects.create(
            user=user)
        user = authenticate(
            username=username,
            password=password)
        login(self.request, user)


class DirectorViewSet(UserViewSet):

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id, is_staff=True)

    def perform_create(self, serializer):
        password = serializer.data['password']
        username = serializer.data['username']
        user = serializer.save()
        user.is_staff = True
        user.save()
        user = authenticate(
            username=username,
            password=password)
        login(self.request, user)


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        myPermissions.UpdateOnly)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Actor.objects.all()
        elif self.request.user.is_authenticated():
            try:
                return Actor.objects.filter(
                    id=Actor.objects.get(
                        user_id=self.request.user.id).id)
            except:
                return Actor.objects.none()
        else:
            return Actor.objects.none()


class RequestContactInfoViewSet(viewsets.ModelViewSet):
    queryset = RequestContactInfo.objects.all()
    serializer_class = RequestContactInfoSerializer
    permission_classes = (
        permissions.IsAuthenticated, myPermissions.IsStaffOrTargetUser,
        myPermissions.PreventUpdate)

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return RequestContactInfo.objects.filter(
                director=self.request.user)
        else:
            return

    def perform_create(self, serializer):
        requests = RequestContactInfo.objects.all()
        actor_id = self.request.data['actor_id']
        actors = Actor.objects.all()

        for r in requests:
            if ((r.director == self.request.user) and
                    (r.actor_id == actor_id)):
                raise serializers.ValidationError(
                    'You have already sent a request to this actor.')
        # if self.request.user == actor:
        #     raise serializers.ValidationError(
        #                 'You cannot send a request to yourself.')
        try:
            actor = Actor.objects.get(id=actor_id)
        except:
            raise serializers.ValidationError(
                'Invalid actor. Please try again.')
        # if user.is_staff:
        #     print "sdaads"
        #     raise serializers.ValidationError(
        #         'You cannot send a request to another director.')

        for a in actors:
            if a.id == actor.id:
                serializer.save(director=self.request.user)
                return
        raise serializers.ValidationError(
                            'Invalid actor. Please try again.')

    @list_route(methods=['get'])
    def confirm_all(self, request, pk=None):
        user = request.user
        requests = RequestContactInfo.objects.filter(
            director_id=user.id, status="pending checkout")
        if requests:
            subject = "Contact info Request"
            html_content = (
                """
                <html>
                <body>
                User Requesting: %s <br>
                User's email: %s <br><br>
                Requested actors contact info: <br><br>
                """
                % (user.username, user.email))

            for r in requests:
                actor = Actor.objects.get(id=r.actor_id)
                r.status = "pending admin approval"
                r.save()
                html_content += (
                    """
                    &nbsp; &nbsp; &nbsp; - %s %s <br>
                    """
                    % (actor.first_name if actor.first_name else "",
                       actor.last_name if actor.last_name else ""))
            html_content += (
                """
                </body>
                </html>
                """)
            email = EmailMultiAlternatives(
                subject, subject, to=['mostafa.93.mahmoud@gmail.com'])
            email.attach_alternative(html_content, "text/html")
            email.send()
        else:
            raise serializers.ValidationError(
                'Invalid')
        pass


def get_token(request):
    """
    Returns the CSRF token required for a POST form. The token is an
    alphanumeric value.

    A side effect of calling this function is to make the csrf_protect
    decorator and the CsrfViewMiddleware add a CSRF cookie and a 'Vary: Cookie'
    header to the outgoing response.  For this reason, you may need to use this
    function lazily, as is done by the csrf context processor.
    """
    request.META["CSRF_COOKIE_USED"] = True
    csrf = request.META.get("CSRF_COOKIE", None)
    return JsonResponse({'csrf': csrf})
