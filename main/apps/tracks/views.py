from ast import Is
from operator import is_
from urllib import request
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.artists.models import Artist
from .models import Track, TrackArtist
from .serializers import TrackSerializer, TrackArtistSerializer
from .permissions import IsArtistUser, IsTrackOwner
from rest_framework.decorators import action, permission_classes as pc
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from apps.albums.models import Album



class TrackViewSet(GenericViewSet):
    serializer_class = TrackSerializer
    permission_classes = [] 
    queryset = Track.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        match self.action:
            case 'create' | 'upload':
                permission_classes = [IsAuthenticated, IsArtistUser]
            case 'update' | 'partial_update' | 'destroy' | 'save_track_artist' | 'delete_track_artist':
                permission_classes = [IsAuthenticated, IsArtistUser, IsTrackOwner]
            case _:  # Mặc định (list, retrieve, get_track_artists, ...)
                permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    # get api/tracks/
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        # track_datas = self.queryset
        # track_datas = self.get_queryset()
        track_datas = Track.objects.all()

        # Get search query from request parameters
        search_query = request.query_params.get('search', '')
        
        if search_query:
            # Filter tracks by title containing search query (case-insensitive)
            track_datas = track_datas.filter(title__icontains=search_query)

        page = self.paginate_queryset(track_datas)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(track_datas, many=True)
        return Response(serializer.data)
    
    # post api/tracks/
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
    
    # get api/tracks/{id}/
    def retrieve(self, request, *args, **kwargs):
        # instance = Track.objects.get(pk=kwargs['pk']) # this is ok too
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # put api/tracks/{id}/
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    # Patch api/tracks/{id}/
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # delete api/tracks/{id}/
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def get_track_artists(self, request, pk=None):
        insance = Track.objects.get(id=pk)
        if not insance:
            return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(insance)
        track_artists = insance.credited_artists.all()
        return Response({
            'track': serializer.data,
            'track_artists': TrackArtistSerializer(track_artists, many=True).data
        })
        
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload track with audio file"""
        try:
            audio_file = request.FILES.get('audio_file')
            if not audio_file:
                return Response(
                    {'error': 'No audio file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if not request.data.get('album_id'):
                album = Album.objects.create(
                    title=request.data.get('album_title'),
                    artist=request.user.artist_profile, 
                )
            else:
                album = get_object_or_404(Album, id=request.data.get('album_id'))
            
            # Get track data from request
            track_data = {
                'title': request.data.get('title'),
                'duration_ms': request.data.get('duration_ms', 0),
                'language': request.data.get('language', ''),
                'plain_lyrics': request.data.get('lyrics', ''),
                'is_instrumental': request.data.get('is_instrumental', False),
                'audio_file_path': audio_file
            }

            # Create track using serializer
            serializer = self.get_serializer(data=track_data)
            if serializer.is_valid():
                serializer.save(artist=request.user.artist_profile,
                                album=album)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=True, methods=['post'])
    def save_track_artist(self, request, pk=None):    
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({'error': 'Artist ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if artist_id == request.user.artist_profile.id:
            return Response({'error': 'Cannot add yourself as a collaborator'}, status=status.HTTP_400_BAD_REQUEST)
        
        role = request.data.get('role', 'featured')  # Default role is 'featured'

        try:
            instance = self.get_object()    
            artist = Artist.objects.get(id=artist_id)
            track_artist = TrackArtist.objects.create(artist=artist, track=instance, role=role)
            serializer = TrackArtistSerializer(track_artist)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        
    @action(detail=True, methods=['delete'])
    def delete_track_artist(self, request, pk=None):
        artist_id = request.data.get('artist_id')
        if not artist_id:
            return Response({'error': 'Artist ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = self.get_object()
            track_artist = TrackArtist.objects.get(track=instance, artist__id=artist_id)
            track_artist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TrackArtist.DoesNotExist:
            return Response({'error': 'Track artist not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    

class TrackArtistViewSet(ModelViewSet):
    queryset = TrackArtist.objects.all()
    serializer_class = TrackArtistSerializer