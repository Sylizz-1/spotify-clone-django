from rest_framework.viewsets import ViewSet
from .models import (
    Folder
)
from .serializers import (
    FolderSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class FolderViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def add_folder(self, request):
        """Thêm folder"""
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def remove_folder(self, request):
        """Xóa folder"""
        folder_id = request.data.get('folder_id')
        if not folder_id:
            return Response({"error": "Folder ID is required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(Folder, id=folder_id, owner=request.user).delete()
        return Response({"message": "Folder removed", "status": "success"}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'])
    def add_folder_to_folder(self, request):
        """Thêm folder vào folder"""
        parent_folder_id = request.data.get('parent_folder_id')
        folder_id = request.data.get('folder_id')
        if not parent_folder_id or not folder_id:
            return Response({"error": "Parent Folder ID and Folder ID are required", "status": "fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        parent_folder = get_object_or_404(Folder, id=parent_folder_id, owner=request.user)
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
        folder.parent = parent_folder
        folder.save()
        return Response({"message": "Folder added to parent folder", "status": "success"}, status=status.HTTP_200_OK)