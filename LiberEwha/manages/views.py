from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from booths.models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied

class ManageBoothView(views.APIView):
    permission_classes= [IsAuthenticated]

    
    def post(self, request, pk):
        serializer = ManageBoothSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 부스 정보 저장
            return Response({'message': '부스 생성 성공', 
                             'data': serializer.data}, 
                            status=HTTP_200_OK)
        return Response({'message': '부스 생성 실패', 
                         'errors': serializer.errors}, 
                        status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk) 
        serializer = ManageBoothSerializer(booth,
                                           data=request.data,
                                           partial=True) #일부만 수정 가능하게: partial=True
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': '부스 수정 성공', 
                             'data': serializer.data}, 
                            status=HTTP_200_OK)
        return Response({'message': '부스 수정 실패', 
                         'errors': serializer.errors}, 
                        status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booth = get_object_or_404(Booth, pk=pk) 
        booth.delete()
        return Response({'message': '부스 삭제 성공'}, 
                        status=HTTP_200_OK )
    
class ManageMenuView(views.APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request, booth_id):
        booth = get_object_or_404(Booth, pk=booth_id)  # 부스가 존재하는지 확인
        serializer = ManageMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(booth=booth)  # 부스 정보 저장
            return Response({'message': '메뉴 생성 성공', 
                             'data': serializer.data}, 
                            status=HTTP_200_OK)
        return Response({'message': '메뉴 생성 실패', 
                         'errors': serializer.errors}, 
                        status=HTTP_400_BAD_REQUEST)

    def patch(self, request, booth_id, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id, booth__id=booth_id) 
        serializer = ManageMenuSerializer(menu,
                                          data=request.data,
                                          partial=True) #일부만 수정 가능하게: partial=True
        if serializer.is_valid():
            updated_menu = serializer.save()
            return Response({'message': '메뉴 수정 성공', 
                             'data': serializer.data}, 
                            status=HTTP_200_OK)
        return Response({'message': '메뉴 수정 실패', 
                         'errors': serializer.errors}, 
                        status=HTTP_400_BAD_REQUEST)

    def delete(self, request, booth_id, menu_id):
        menu = get_object_or_404(Menu, pk=menu_id, booth__id=booth_id) 
        menu.delete()
        return Response({'message': '메뉴 삭제 성공'}, 
                        status=HTTP_200_OK )
    
class ManageView(views.APIView): #부스 상세 페이지
    permission_classes= [IsAuthenticated]

    serializer_class = ManageSerializer

    def get(self, request):
        
        is_show= request.GET.get('is_show')

        # 부스 정렬 기준
        booths = Booth.objects.all()

        if is_show == 'False':
                booths = booths.filter(is_show = False)
        else:
                booths = booths.filter(is_show=True)

        booths = booths.order_by("id") #오름차순 정렬
        serializer = ManageSerializer(booths, many=True)
        return Response({'message': "TF - 목록 불러오기 성공",
                         'data': serializer.data},
                        status=HTTP_200_OK)