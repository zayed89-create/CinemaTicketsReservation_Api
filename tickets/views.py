from django.shortcuts import render
from django.http.response import JsonResponse
# Create your views here.
from .models import Guest,Reservation,Movie,Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializer,ReservationSerializer,MovieSerializer,PostSerializer
from rest_framework import status,filters,generics,mixins,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
def no_rest_no_model(request):
    quests = [
        {'id':1,
         'Name':'zayed',
         'mobile':12547
         },
        {'id':2,
         'Name':'zizo',
         'mobile':12547
         },
    ]
    return JsonResponse(quests, safe= False)

def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guest':list(data.values('name','mobile'))
    }
    return JsonResponse(response)


@api_view(['POST','GET'])
def FBV_LIST(request):
    if request.method == 'GET':
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.data,status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['GET','PUT','DELETE'])       
def FBV_PK(request,pk) :

    try:
      guest=Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
       return Response (status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer=GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
       
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class CBV_LIST(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status.HTTP_400_BAD_REQUEST)
       
class CBV_pk(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    def put(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
         guest = self.get_object(pk)
         guest.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
        
                      
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    
class Mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    def post(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.delete(request)
    
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
        
        
    
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
        
  
        
        
  
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
   
        
class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']
    
class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer
    
@api_view(['GET'])
def find_movie(request):
    movies=Movie.objects.filter(
        movie = request.data['movie'],
        hall = request.data['hall']
    )    
    serializer = MovieSerializer(movies,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def new_reservation(request):
    movie=Movie.objects.get(
        movie = request.data['movie'],
        hall = request.data['hall']
    )   
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()
    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)
        
            
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
                