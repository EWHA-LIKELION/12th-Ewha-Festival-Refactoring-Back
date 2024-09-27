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
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
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
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
        booth.delete()
        return Response({'message': '부스 삭제 성공'}, 
                        status=HTTP_200_OK )
    
class ManageMenuView(views.APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request, booth_id):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=booth_id)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
        #booth = get_object_or_404(Booth, pk=booth_id)  # 부스가 존재하는지 확인
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
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, booth__id=booth_id)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
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
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, booth__id=booth_id)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
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
    
class ReplyManageView(views.APIView):
    permission_classes = [IsAuthenticated]
    # 로그인하지 않으면 401 Unauthorized 뜸

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)

    def post(self, request, pk, guestbook_id, format=None):
        # 해당 부스의 관리자인지 확인
        booth = self.get_object(pk)
        if booth.user != request.user:
            return Response({"error": "해당 부스 관리자만 답글을 달 수 있습니다."}, 
                            status=HTTP_403_FORBIDDEN)
        
        try:
            guestbook_entry = Guestbook.objects.get(id=guestbook_id, booth=booth)
        except Guestbook.DoesNotExist:
            return Response({"error": "해당 방명록 항목을 찾을 수 없습니다."},
                            status=HTTP_404_NOT_FOUND)
        
        serializer = ReplySerializer(data=request.data, context={'request': request, 'guestbook_id': guestbook_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "답글 작성 성공!",
                            "data": serializer.data}, 
                            status=HTTP_201_CREATED)
        
        return Response({"error": "답글 작성 실패"}, 
                            status=HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, guestbook_id, format=None):
        booth = self.get_object(pk)
        try:
            guestbook_entry = Guestbook.objects.get(id=guestbook_id, booth=booth)
        except Guestbook.DoesNotExist:
            return Response({"error": "해당 방명록 항목을 찾을 수 없습니다."},
                            status=HTTP_404_NOT_FOUND)
        
        replies = Reply.objects.filter(guestbook=guestbook_entry)
        serializer = ReplySerializer(replies, many=True)

        return Response({"message": "방명록 답글 가져오기 성공!", 
                        "data": serializer.data}, 
                        status=HTTP_200_OK)
    
class ReplyDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Booth, pk=pk)

    def delete(self, request, pk, guestbook_id, reply_id):
        booth = self.get_object(pk)
        guestbook_entry = get_object_or_404(Guestbook, id=guestbook_id, booth=booth)
        reply_entry = get_object_or_404(Reply, id=reply_id, guestbook=guestbook_entry)

        if reply_entry.user != request.user:
            return Response({"error": "자신이 작성한 댓글만 삭제할 수 있습니다."}, 
                            status=HTTP_403_FORBIDDEN)
        
        reply_entry.delete()
        return Response({"message": "답글 삭제 성공!"}, 
                        status=HTTP_204_NO_CONTENT)
    
class NoticeView(views.APIView):
    def post(self, request, pk):
        # 로그인이 되어있는지
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        booth = get_object_or_404(Booth, pk=pk)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
        data = request.data
        data['booth'] = booth.id
    
        serializer = BoothNoticeSerializer(data = data)
        if serializer.is_valid():
            booth.increaseNoticeCount()
            serializer.save()
            return Response({'message': '공지를 등록했습니다.'}, status=HTTP_200_OK)
    
        else:
            return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)
        
        booth = get_object_or_404(Booth, pk = pk)
        boothSerializer = BoothNoticeCountSerializer(booth)

        notice_list = {}
        
        notices = Booth_notice.objects.filter(booth = pk)
        i=0
        for notice in notices:
            i += 1
            noticeSerializer = BoothNoticeSerializer(notice)
            notice_list[i] = noticeSerializer.data
            



        return Response({
            "count": boothSerializer.data,
            "notice": notice_list
        }, status=HTTP_200_OK)

class NoticeDeleteView(views.APIView):
    def delete(self, request, pk, info_id):
        if not request.user.is_authenticated:
            return Response({"message": "로그인이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        boothNotice = get_object_or_404(Booth_notice, pk=info_id)
        booth = get_object_or_404(Booth, pk=pk)

        # 부스의 user가 내가 맞는지
        if request.user != booth.user:
            return Response({"message": "권한이 없습니다."}, status=HTTP_400_BAD_REQUEST)
    
        booth.decreaseNoticeCount()
        boothNotice.delete()
        return Response({"message": "공지 삭제"}, status=HTTP_200_OK)
