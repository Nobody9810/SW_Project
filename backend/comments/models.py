from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

class Comment(models.Model):
    """通用评论模型"""
    # 关联文章
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # 用户信息 (支持匿名)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    nickname = models.CharField(_("昵称"), max_length=50, default="匿名书友")
    
    # 内容
    content = models.TextField(_("评论内容"))
    
    # 父评论 (实现盖楼/回复)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    # 元数据
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(_("是否显示"), default=True) # 软删除

    class Meta:
        ordering = ['-created_at'] # 最新评论在前
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.nickname}: {self.content[:20]}..."