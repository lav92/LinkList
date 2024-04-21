from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.response import Response
from django.forms.models import model_to_dict
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login, logout
from django.http import Http404

from links.serializers import UserSerializer, LinkSerializer, CollectionSerializer
from links.models import Link, Collection
from links.services import get_url_data

"""
    Users Views
"""


class RegistrationView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        user = User(**request.data)
        user.set_password(request.data.get('password'))
        user.save()
        return Response(model_to_dict(user))


class LoginView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer}
    )
    def post(self, request):
        user = User.objects.get(email=request.data.get('email'))
        if user.check_password(request.data.get('password')):
            login(request, user)
            return Response(model_to_dict(user))
        else:
            return Response(status=401, data="Неверный пароль")


class ChangePassword(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        examples=[
            OpenApiExample(
                name="Change password",
                description="Change password",
                value=
                {
                    "old_password": "oldpassword",
                    "new_password": "newpassword",
                },
            ),
        ],
    )
    def post(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response(status=401, data='Авторизуйтесь')
        else:
            if not request.user.check_password(request.data.get('old_password')):
                return Response(status=401, data={"Вы ввели неверный старый пароль"})
            else:
                request.user.set_password(request.data.get('new_password'))
                request.user.save()
                return Response(data="Вы успешно поменяли пароль")


class MyAccountView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer}
    )
    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return Response(status=401, data='Авторизуйтесь')
        else:
            return Response(model_to_dict(request.user))


class LogoutView(APIView):
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer}
    )
    def get(self, request):
        logout(request)
        return Response(data={"Вы вышли из системы"})


"""
    Links Views
"""


class LinkCreateView(CreateAPIView):
    @extend_schema(
        request=LinkSerializer,
        responses={201: LinkSerializer},

        examples=[
            OpenApiExample(
                name="Create link",
                description="Добавление ссылки",
                value={
                    "url": "http://example.com"
                },
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response(status=401, data='Авторизуйтесь')
        elif Link.objects.filter(url=request.data.get('url'), owners=request.user).exists():
            return Response(status=409, data="У вас уже есть данная ссылка")
        else:
            try:
                url_data = get_url_data(request.data.get('url'))
            except ValueError as e:
                return Response(status=400, data=str(e))
            link = Link.objects.create(
                url=request.data.get('url'),
                **url_data
            )
            link.owners = self.request.user
            link.save()
            return Response(data=f"Ссылка {link.title} добавлена", status=201)


class AllLinksView(ListAPIView):
    serializer_class = LinkSerializer

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            raise Http404("Авторизуйтесь")
        return Link.objects.filter(owners=self.request.user)


class SingleLinkView(RetrieveAPIView):
    serializer_class = LinkSerializer

    def get_object(self):
        return get_object_or_404(Link, pk=self.kwargs.get('pk'), owners=self.request.user)


class UpdateLinkView(UpdateAPIView):
    serializer_class = LinkSerializer

    def get_object(self):
        return get_object_or_404(Link, pk=self.kwargs.get('pk'), owners=self.request.user)


class DeleteLinkView(DestroyAPIView):
    serializer_class = LinkSerializer

    def get_object(self):
        return get_object_or_404(Link, pk=self.kwargs.get('pk'), owners=self.request.user)


class LinkToCollection(APIView):
    @extend_schema(
        request=LinkSerializer,
        responses={201: LinkSerializer},

        examples=[
            OpenApiExample(
                name="Link to Collection",
                description="Добавлние ссылки в коллекцию",
                value={
                    "link_name": "link_name",
                    "collection_name": "collection_name",
                },
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        links = Link.objects.filter(title="Про программирование", owners=request.user)
        collections = Collection.objects.filter(title=request.data.get('collection_name'), owners=request.user)

        if isinstance(request.user, AnonymousUser):
            return Response(status=401, data='Авторизуйтесь')
        elif not links.exists():
            return Response(status=409, data="У вас нет ссылки с таким именем")
        elif not collections.exists():
            return Response(status=409, data="У вас нет коллекции с таким именем")
        else:
            link, collection = links[0], collections[0]
            link.collections.add(collection)
            return Response(data=f"Ссылка {link.title} добавлена в коллекцию {collection.title}", status=201)


"""
    Collections Views
"""


class CollectionCreateView(CreateAPIView):
    serializer_class = CollectionSerializer

    def perform_create(self, serializer):
        serializer.save(owners=self.request.user)


class AllCollectionView(ListAPIView):
    serializer_class = CollectionSerializer

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            raise Http404("Авторизуйтесь")
        return Collection.objects.filter(owners=self.request.user)


class SingleCollectionView(RetrieveAPIView):
    serializer_class = CollectionSerializer

    def get_object(self):
        return get_object_or_404(Collection, pk=self.kwargs.get('pk'), owners=self.request.user)


class UpdateCollectionView(UpdateAPIView):
    serializer_class = CollectionSerializer

    def get_object(self):
        return get_object_or_404(Collection, pk=self.kwargs.get('pk'), owners=self.request.user)


class DeleteCollectionView(DestroyAPIView):
    serializer_class = CollectionSerializer

    def get_object(self):
        return get_object_or_404(Collection, pk=self.kwargs.get('pk'), owners=self.request.user)
