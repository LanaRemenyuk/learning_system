from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from .models import CustomUser, Lesson, Product, Watched
from .permissions import IsOwnerAdminOrReadOnly
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer, CustomUserCreateSerializer, LessonSerializer, WatchedSerializer
from django.db.models import Sum, Count
from django.http import JsonResponse

class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_fields = ["username"]
    lookup_field = "username"

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated, IsOwnerAdminOrReadOnly],
    )
    def read(self, request):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if request.method == "GET":
            serializer = CustomUserSerializer(user, many=False)
            return Response(serializer.data)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsOwnerAdminOrReadOnly)
    )
    def post_prod(self, request, id):
        user = request.user
        owner = get_object_or_404(CustomUser, id=id)
        product = Product.objects.create(
            owner=owner,
            user=user,
        )
        product.save()
        return Response(f'You added {product}',
                        status=status.HTTP_201_CREATED)


    def delete_prod(self, request, id):
        user = request.user
        owner = get_object_or_404(CustomUser, id=id)
        delete_prod = Product.objects.filter(
            user=user.id, owner=owner.id
        )
        delete_prod.delete()
        return Response(f'You deleted {delete_prod}',
                        status=status.HTTP_204_NO_CONTENT)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('product')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)


class WatchedViewSet(viewsets.ModelViewSet):
    queryset = Watched.objects.all()
    serializer_class = WatchedSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)


def get_stat(request):
    total_watched = Lesson.objects.filter(watched__if_watched='True').count()
    total_students = Product.objects.all().aggregate(Count('subscriber'))
    response = {
        'total_watched': total_watched,
        'total_students': total_students

    }

    return JsonResponse(response)



