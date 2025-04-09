from rest_framework.viewsets import ViewSet
from .models import (
    UserFollowedArtist, UserFollowedPodcast, UserFollowedPlaylist,
    UserSavedTrack, UserSavedEpisode, Folder, Playlist
)
from .serializers import (
    FolderSerializer,
    PlaylistSerializer
)
from apps.tracks.serializers import TrackSerializer
from apps.tracks.models import Track
from apps.artists.serializers import ArtistSerializer
from apps.artists.models import Artist
from apps.podcasts.models import PodcastEpisode, Podcast
from apps.podcasts.serializers import PodcastSerializer, PodcastEpisodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import secrets
import datetime



class PlaylistViewSet(ViewSet):
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def add_playlist(self, request):
        """Thêm playlist"""
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            UserFollowedPlaylist.objects.create(user=request.user, playlist=serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def update_playlist(self, request):
        """Cập nhật playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def add_playlist_to_folder(self, request):
        """Thêm playlist vào folder"""
        playlist_id = request.data.get('playlist_id')
        folder_id = request.data.get('folder_id')
        if not playlist_id or not folder_id:
            return Response({"error": "Playlist ID and Folder ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        folder = Folder.objects.filter(id=folder_id, owner=request.user).first()
        if not playlist or not folder:
            return Response({"error": "Playlist or Folder not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist).update(folder=folder)
        return Response({"message": "Playlist added to folder", "status": "success"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['put'])
    def remove_playlist_from_folder(self, request):
        """Xóa playlist khỏi folder"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist).update(folder=None)
        return Response({"message": "Playlist removed from folder", "status": "success"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_playlists(self, request):
        """Lấy danh sách playlist"""
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_playlist(self, request):
        """Lấy thông tin playlist"""
        playlist_id = request.query_params.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'])
    def remove_playlist(self, request):
        """Xóa playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        Playlist.objects.filter(id=playlist_id, user=request.user).delete()
        return Response({"message": "Playlist removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def follow_playlist(self, request):
        """Theo dõi playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)

        playlist = Playlist.objects.filter(id=playlist_id).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)

        UserFollowedPlaylist.objects.get_or_create(user=request.user, playlist=playlist)
        return Response({"message": "Playlist followed", "status": "success"}, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['delete'])
    def unfollow_playlist(self, request):
        """Bỏ theo dõi playlist"""
        playlist_id = request.data.get('playlist_id')
        if not playlist_id:
            return Response({"error": "Playlist ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        playlist = Playlist.objects.filter(id=playlist_id).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        followed_playlist = UserFollowedPlaylist.objects.filter(user=request.user, playlist=playlist)
        if followed_playlist.user == request.user:
            return Response({"error": "You cannot unfollow your playlist", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        followed_playlist.delete()
        return Response({"message": "Playlist unfollowed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)
    
    # ------------------------------ Playlist Items ------------------------------
    @action(detail=False, methods=['post'])
    def add_item_to_playlist(self, request):
        """Thêm item vào playlist"""
        playlist_id = request.data.get('playlist_id')
        item_type = request.data.get('item_type')
        item_id = request.data.get('item_id')
        item = None
        if item_type == 'track':
            item = get_object_or_404(Track, id=item_id)
        elif item_type == 'podcast_episode':
            item = get_object_or_404(PodcastEpisode, id=item_id)
        
        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist.items:
            playlist.items = []
        
        playlist.items.append({
            "uid": secrets.token_hex(8),
            "item_type": item_type,
            "item_id": str(item.id),
            "item_name": item.title,
            "owner_id": str(item.artist.id) if item_type == 'track' else str(item.podcast.podcaster.id),
            "owner_name": item.artist.name if item_type == 'track' else item.podcast.podcaster.name,
            "album_or_podcast": item.album.title if item_type == 'track' else item.podcast.title,
            "album_or_podcast_id": str(item.album.id) if item_type == 'track' else str(item.podcast.id),
            "item_image":   item.album.avatar_url.url
                            if item_type == 'track' and item.album and item.album.avatar_url 
                            else item.cover_art_image_url.url 
                            if item_type == 'podcast_episode' and item.cover_art_image_url 
                            else '',
            "item_duration_ms": item.duration_ms,
            "created_at": datetime.datetime.now().isoformat(),
        })
        
        playlist.save()
        return Response({"message": "Item added to playlist", "status": "success",
                         "data": playlist.items[-1] }, status=status.HTTP_201_CREATED)
        
        
    @action(detail=False, methods=['put'])
    def change_item_order(self, request):
        """Thay đổi thứ tự item trong playlist"""
        playlist_id = request.data.get('playlist_id')
        uids = request.data.get('uids', [])
        move_type = request.data.get('move_type')
        from_uid = request.data.get('from_uid')
        
        playlist = Playlist.objects.filter(id=playlist_id, user=request.user).first()
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        items = playlist.items
        moving_items = [item for item in items if item['uid'] in uids]
        items = [item for item in items if item['uid'] not in uids]
        targed_item = [item for item in items if item['uid'] == from_uid][0]
        index_inserting = items.index(targed_item) + 1 if move_type == 'after' else items.index(targed_item)
        items = items[:index_inserting] + moving_items + items[index_inserting:]
        playlist.items = items
        playlist.save()
        return Response({"message": "Item order changed", "status": "success",
                         "data": playlist.items }, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['delete'])
    def remove_item_from_playlist(self, request):
        """Xóa item khỏi playlist"""
        playlist_id = request.data.get('playlist_id')
        item_uid = request.data.get('item_uid')
        
        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        if not playlist:
            return Response({"error": "Playlist not found", "status": "fail"}, status=status.HTTP_404_NOT_FOUND)
        
        items = playlist.items
        items = [item for item in items if item['uid'] != item_uid]
        playlist.items = items
        playlist.save()
        return Response({"message": "Item removed from playlist", "status": "success",
                         "data": playlist.items }, status=status.HTTP_200_OK)
