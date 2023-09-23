from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from .models import CustomUser, Lesson, Product, Watched
from .permissions import IsOwnerAdminOrReadOnly
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CustomUserSerializer, ProductSerializer, LessonSerializer, WatchedSerializer
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)
    filterset_fields = ('name')


class WatchedViewSet(viewsets.ModelViewSet):
    queryset = Watched.objects.all()
    serializer_class = WatchedSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)
    filterset_fields = ('product', 'username')


def get_stat(request):
    total_watched = Lesson.objects.filter(watched__if_watched='True').count()
    total_students = Product.objects.filter(subscriber__product=True).count()
    users_number = CustomUser.objects.count()
    sales_percentage = round(total_students/users_number*100)
    tesst = Watched.objects.filter(time__isnull=False)
    count = 0
    for i in tesst:
        count += i.time.total_seconds()
    response = {
        'total_watched': total_watched,
        'total_students': total_students,
        'users_number': users_number,
        'sales_percentage': sales_percentage,
        'count': int(count)
    }
    return JsonResponse(response)



