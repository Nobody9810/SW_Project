from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserReaction

class ReactionViewSet(viewsets.ViewSet):
    """
    处理点赞/点踩逻辑
    API: POST /api/reactions/toggle/
    Body: {
        "model": "news",      # 文章类型 (model_name)
        "id": 1,              # 文章ID
        "type": "like"        # or "dislike"
    }
    """
    permission_classes = [permissions.AllowAny] # 允许匿名

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        # 1. 获取参数
        model_name = request.data.get('model')
        object_id = request.data.get('id')
        reaction_type = request.data.get('type')

        if reaction_type not in ['like', 'dislike']:
            return Response({"error": "Invalid type"}, status=400)

        # 2. 获取 ContentType
        try:
            ct = ContentType.objects.get(app_label='articles', model=model_name)
        except ContentType.DoesNotExist:
            return Response({"error": "Object not found"}, status=404)

        model_class = ct.model_class()
        try:
            obj = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            return Response({"error": "Object not found"}, status=404)

        # 3. 识别用户 (Session 策略)
        user = request.user if request.user.is_authenticated else None
        if not request.session.session_key:
            request.session.save() # 强制生成 session_key
        session_key = request.session.session_key

        # 查找现有记录
        filter_kwargs = {
            'content_type': ct, 
            'object_id': object_id,
        }
        if user:
            filter_kwargs['user'] = user
        else:
            filter_kwargs['session_key'] = session_key

        existing_reaction = UserReaction.objects.filter(**filter_kwargs).first()

        # 4. 逻辑处理
        # 需要同时更新 UserReaction 表 和 文章本身的 likes/dislikes 计数
        
        response_data = {"action": "created", "current": reaction_type}

        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # 情况A: 点击了相同的按钮 -> 取消 (删除记录)
                existing_reaction.delete()
                # 更新文章计数 (-1)
                if reaction_type == 'like':
                    obj.likes = F('likes') - 1
                else:
                    obj.dislikes = F('dislikes') - 1
                response_data["action"] = "removed"
                response_data["current"] = None
            else:
                # 情况B: 点击了相反的按钮 -> 切换 (更新记录)
                old_type = existing_reaction.reaction_type
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                # 更新文章计数 (+1 new, -1 old)
                if reaction_type == 'like':
                    obj.likes = F('likes') + 1
                    obj.dislikes = F('dislikes') - 1
                else:
                    obj.likes = F('likes') - 1
                    obj.dislikes = F('dislikes') + 1
                response_data["action"] = "switched"
        else:
            # 情况C: 第一次操作 -> 创建
            UserReaction.objects.create(
                user=user,
                session_key=session_key,
                content_type=ct,
                object_id=object_id,
                reaction_type=reaction_type
            )
            # 更新文章计数 (+1)
            if reaction_type == 'like':
                obj.likes = F('likes') + 1
            else:
                obj.dislikes = F('dislikes') + 1

        obj.save(update_fields=['likes', 'dislikes'])
        obj.refresh_from_db()
        
        return Response({
            **response_data,
            "likes": obj.likes,
            "dislikes": obj.dislikes
        })