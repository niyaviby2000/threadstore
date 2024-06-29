from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from api.serializers import UserSerializer,ProductSerializer

from store.models import Product

from django.contrib.auth.models import User

from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet

from rest_framework import authentication

from rest_framework import permissions

# from api.permissions import OwnerOnly

class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()


            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        

class ProductViewSetView(ModelViewSet):

    serializer_class=ProductSerializer

    queryset=Product.objects.all()

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    # permission_classes=[OwnerOnly]

    # def list(self,request,*args,**kwargs):

    #     qs=Product.objects.filter(user_object=request.user)

    #     serializer_instance=ProductSerializer(qs,many=True)

    #     return Response(data=serializer_instance.data)
    
    # def perform_create(self, serializer):

    #     return serializer.save(user_object=self.request.user)