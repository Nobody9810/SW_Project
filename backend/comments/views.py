from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer

class CommentViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    评论接口
    GET /api/comments/?model=news&id=1  -> 获取某文章的评论
    POST /api/comments/                 -> 发表评论
    """
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """根据 URL 参数过滤评论"""
        queryset = Comment.objects.filter(is_active=True, parent=None) # 只获取顶级评论
        
        model_name = self.request.query_params.get('model')
        object_id = self.request.query_params.get('id')
        
        if model_name and object_id:
            try:
                ct = ContentType.objects.get(app_label='articles', model=model_name)
                queryset = queryset.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                return Comment.objects.none()
                
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        """创建时注入用户信息"""
        user = self.request.user if self.request.user.is_authenticated else None
        
        # 处理 Session
        if not self.request.session.session_key:
            self.request.session.save()
        session_key = self.request.session.session_key

        # 自动生成昵称逻辑 (如果有登录则用用户名，否则叫"书友+Session后缀")
        nickname = "匿名书友"
        if user:
            nickname = getattr(user, 'username', '用户')
        else:
            nickname = f"书友_{session_key[-4:]}" # 取 Session 后4位区分
            
        # 如果用户手动填了昵称 (你可以在前端开放这个输入框)，则优先使用
        if 'nickname' in self.request.data and self.request.data['nickname']:
            nickname = self.request.data['nickname']

        serializer.save(
            user=user,
            session_key=session_key,
            nickname=nickname
        )