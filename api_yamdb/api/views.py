from django.forms import ValidationError
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from reviews.models import User
from .serializers import AuthSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAdminUser, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    # @action(detail=True, methods=['get', 'patch']) #permission_classes=[IsAuthenticated])
    # def me(self, request, pk=None):

    #     if request.method == 'POST':
    #         serializer = UserSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     profile_username = User.objects.filter(
    #         username=self.request.user.username)
    #     serializer = UserSerializer(profile_username)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class SignupViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [permissions.AllowAny, ]
    


        
        
    # @action(detail=False,  methods=['post']
    # def token(self, request):
        # user_id = request.query_params.get('user_id', '')
        # confirmation_token = request.query_params.get('confirmation_token', '')
        # try:
        #     user = self.get_queryset().get(pk=user_id)
        # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
   #     user = None
        # if user is None:
        #     return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
         # if not default_token_generator.check_token(user, confirmation_token):
       #     return Response('Token is invalid or expired. Please request another confirmation email by signing in.', status=status.HTTP_400_BAD_REQUEST)
        # user.is_active = True
        # user.save()
            # return Response('Email successfully confirmed')