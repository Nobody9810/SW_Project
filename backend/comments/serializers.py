from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    
    # 显示子评论 (简单嵌套，适用于 UI 直接渲染)
    # 如果评论量巨大，建议前端分开请求，这里演示一次性返回子评论
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'nickname', 'content', 'created_at', 
            'parent', 'replies'
        ]
        read_only_fields = ['nickname'] # 昵称由后端逻辑生成

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_active=True), many=True).data
        return []

class CommentCreateSerializer(serializers.ModelSerializer):
    """创建评论专用的 Serializer"""
    model = serializers.CharField(write_only=True) # 接收 'news', 'paper' 等字符串
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['model', 'object_id', 'content', 'parent', 'nickname']

    def create(self, validated_data):
        model_name = validated_data.pop('model')
        object_id = validated_data.pop('object_id')
        
        # 查找 ContentType
        try:
            ct = ContentType.objects.get(app_label='articles', model=model_name)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("无效的文章类型")

        # 注入 ContentType
        validated_data['content_type'] = ct
        validated_data['object_id'] = object_id
        
        return super().create(validated_data)