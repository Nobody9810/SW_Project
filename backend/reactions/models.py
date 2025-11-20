from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class UserReaction(models.Model):
    """用户反应记录表"""
    LIKE = 'like'
    DISLIKE = 'dislike'
    
    REACTION_CHOICES = [
        (LIKE, _('点赞')),
        (DISLIKE, _('点踩')),
    ]

    # 1. 谁产生的反应？(登录用户 或 匿名Session)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        db_index=True
    )
    session_key = models.CharField(_("Session ID"), max_length=40, blank=True, null=True, db_index=True)

    # 2. 对什么产生的反应？(通用关联)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # 3. 具体反应
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 联合唯一索引：确保一个用户(或Session)对同一对象只能有一条记录
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['session_key', 'content_type', 'object_id']),
        ]

    def __str__(self):
        who = self.user.username if self.user else f"Anon({self.session_key})"
        return f"{who} {self.reaction_type} -> {self.content_type} id={self.object_id}"