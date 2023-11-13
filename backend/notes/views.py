from django.utils import timezone
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NoteSerializer, UserSerializer
from .models import Note, User


class NoteView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateNoteView(APIView):
    def post(self, request):
        note_text = request.data.get('note_text')
        owner_id = request.data.get('owner')  # Assuming owner is an ID
        print(note_text, owner_id)
        try:
            owner = User.objects.get(id=owner_id)
            Note.objects.create(
                note_text=note_text,
                pub_date=timezone.now(),
                owner=owner
            )
            return Response({'message': 'Note created successfully'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'})

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HandleUserConnction(APIView):

    
    queryset = User.objects.all()



    
    def get(self, request):
        
        login = request.get('login')
        password = request.get('password')  # Assuming owner is an ID
        
        try:
            
            if (User.objects.raw('SELECT count(*) FROM notes_user WHERE username LIKE "'+login+'" AND password LIKE "'+password+'"') == 1):
            
                return Response({'message': 'Note created successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_418_IM_A_TEAPOT)
        except:
            return Response({'error': 'System error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


