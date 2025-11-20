# articles/models.py

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

# 引入压缩工具
from .utils import compress_image, compress_pdf

# ==================== 抽象基类 (保持不变) ====================

class TimeStampedModel(models.Model):
    """时间戳抽象基类"""
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """可发布模型抽象基类"""
    is_published = models.BooleanField(
        _("是否发布"),
        default=False,
        db_index=True,
        help_text=_("勾选后文章将在前台显示")
    )

    class Meta:
        abstract = True


class ViewCountModel(models.Model):
    """浏览量统计抽象基类"""
    total_views = models.PositiveIntegerField(_("总浏览量"), default=0, db_index=True)
    today_views = models.PositiveIntegerField(_("今日浏览量"), default=0, db_index=True)
    last_view_date = models.DateField(_("最后统计日期"), auto_now=True)

    class Meta:
        abstract = True


class ReactionModel(models.Model):
    """反应（点赞/点踩）抽象基类"""
    likes = models.PositiveIntegerField(_("点赞数"), default=0, db_index=True)
    dislikes = models.PositiveIntegerField(_("点踩数"), default=0, db_index=True)

    class Meta:
        abstract = True


class BaseArticle(TimeStampedModel, PublishableModel, ViewCountModel, ReactionModel):
    """文章基类"""
    title = models.CharField(_("标题"), max_length=200, db_index=True)
    content = models.TextField(_("内容"), blank=True, default="")
    author = models.CharField(_("作者"), max_length=200, blank=True, default="")
    source = models.CharField(_("来源"), max_length=200, blank=True, default="")
    
    # 关联用户反应 (需要 reactions app 已安装)
    reactions = GenericRelation('reactions.UserReaction')

    class Meta:
        abstract = True
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at', 'is_published']),
            models.Index(fields=['is_published', '-total_views']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        model_name = self._meta.model_name
        # 假设前端路由结构，或者 API 详情路由
        return reverse(f'api:articles:{model_name}-detail', args=[str(self.id)])


# ==================== 具体模型 (添加 Save 方法) ====================

class News(BaseArticle):
    """通讯"""
    image = models.ImageField(
        _("图片"),
        upload_to='articles/news/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("通讯")
        verbose_name_plural = _("通讯")
        db_table = 'articles_news'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class BookInfo(BaseArticle):
    """书讯"""
    author_intro = models.TextField(_("作者简介"), blank=True, default="")
    catalog = models.TextField(_("目录"), blank=True, default="")
    preface = models.TextField(_("前言"), blank=True, default="")
    isbn = models.CharField(_("ISBN"), max_length=30, blank=True, default="")
    publisher = models.CharField(_("出版社"), max_length=200, blank=True, default="")
    publish_date = models.DateField(_("出版年份"), blank=True, null=True)
    price = models.CharField(_("定价"), max_length=20, blank=True, default="")
    pages = models.PositiveIntegerField(_("页数"), blank=True, null=True)
    binding = models.CharField(_("装帧"), max_length=50, blank=True, default="")
    image = models.ImageField(
        _("封面图片"),
        upload_to='articles/books/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("书讯")
        verbose_name_plural = _("书讯")
        db_table = 'articles_book_info'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class BookReviewCategory(models.Model):
    """书评分类"""
    name = models.CharField(_("分类名称"), max_length=100, unique=True)
    slug = models.SlugField(_("URL标识"), max_length=100, unique=True)
    description = models.TextField(_("描述"), blank=True, default="")

    class Meta:
        verbose_name = _("书评分类")
        verbose_name_plural = _("书评分类")
        db_table = 'articles_book_review_category'

    def __str__(self):
        return self.name


class BookReview(BaseArticle):
    """书评"""
    book_publish_date = models.DateField(_("书籍出版日期"), blank=True, null=True)
    image = models.ImageField(
        _("图片"),
        upload_to='articles/reviews/%Y/%m/',
        blank=True, null=True
    )
    category = models.ForeignKey(
        BookReviewCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("分类"),
        related_name='reviews'
    )

    class Meta:
        verbose_name = _("书评")
        verbose_name_plural = _("书评")
        db_table = 'articles_book_review'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class Opinion(BaseArticle):
    """观点"""
    image = models.ImageField(
        _("图片"),
        upload_to='articles/opinions/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("观点")
        verbose_name_plural = _("观点")
        db_table = 'articles_opinion'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class Literature(BaseArticle):
    """文艺"""
    image = models.ImageField(
        _("图片"),
        upload_to='articles/literature/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("文艺")
        verbose_name_plural = _("文艺")
        db_table = 'articles_literature'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class QA(BaseArticle):
    """问答"""
    is_approved = models.BooleanField(_("是否通过审核"), default=False, db_index=True)
    author = None # 问答不需要作者字段

    class Meta:
        verbose_name = _("问答")
        verbose_name_plural = _("问答")
        db_table = 'articles_qa'
    
    # QA 没有图片，不需要重写 save


class Translation(BaseArticle):
    """译林"""
    original_title = models.CharField(_("原文标题"), max_length=200)
    original_author = models.CharField(_("原文作者"), max_length=100, blank=True, default="")
    original_publish_date = models.DateField(_("原文出版日期"), blank=True, null=True)
    image = models.ImageField(
        _("图片"),
        upload_to='articles/translations/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("译林")
        verbose_name_plural = _("译林")
        db_table = 'articles_translation'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class History(BaseArticle):
    """文史"""
    image = models.ImageField(
        _("图片"),
        upload_to='articles/history/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("文史")
        verbose_name_plural = _("文史")
        db_table = 'articles_history'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class Paper(BaseArticle):
    """论文"""
    image = models.ImageField(
        _("封面图片"),
        upload_to='articles/papers/images/%Y/%m/',
        blank=True, null=True
    )
    document = models.FileField(
        _("PDF文档"),
        upload_to='articles/papers/docs/%Y/%m/',
        blank=True, null=True
    )
    content = None # 论文没有 content 字段

    class Meta:
        verbose_name = _("论文")
        verbose_name_plural = _("论文")
        db_table = 'articles_paper'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        # 只有当扩展名是 pdf 时才尝试压缩
        if self.document and self.document.name.lower().endswith('.pdf'):
            self.document = compress_pdf(self.document)
        super().save(*args, **kwargs)


class ClassicBook(BaseArticle):
    """古籍"""
    document = models.FileField(
        upload_to='articles/classics/%Y/%m/',
        verbose_name=_("PDF文档")
    )
    content = None

    class Meta:
        verbose_name = _("古籍")
        verbose_name_plural = _("古籍")
        db_table = 'articles_classic_book'

    def save(self, *args, **kwargs):
        if self.document and self.document.name.lower().endswith('.pdf'):
            self.document = compress_pdf(self.document)
        super().save(*args, **kwargs)


class Library(BaseArticle):
    """书库"""
    document = models.FileField(
        _("PDF文档"),
        upload_to='articles/library/%Y/%m/'
    )
    author_intro = models.TextField(_("作者简介"), blank=True, default="")
    content_intro = models.TextField(_("内容简介"), blank=True, default="")
    publish_date = models.DateField(_("出版日期"), blank=True, null=True)
    image = models.ImageField(
        _("封面图片"),
        upload_to='articles/library/images/%Y/%m/',
        blank=True, null=True
    )
    isbn = models.CharField(_("ISBN"), max_length=30, blank=True, default="")

    class Meta:
        verbose_name = _("书库")
        verbose_name_plural = _("书库")
        db_table = 'articles_library'

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        if self.document and self.document.name.lower().endswith('.pdf'):
            self.document = compress_pdf(self.document)
        super().save(*args, **kwargs)


# ==================== 经训相关 ====================

class Scripture(TimeStampedModel, PublishableModel):
    """经训"""
    title = models.CharField(_("标题"), max_length=200)
    image = models.ImageField(
        _("图片"),
        upload_to='articles/scriptures/%Y/%m/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("经训")
        verbose_name_plural = _("经训")
        db_table = 'articles_scripture'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)
        super().save(*args, **kwargs)


class ScriptureChapter(TimeStampedModel, PublishableModel):
    """经训章节"""
    scripture = models.ForeignKey(
        Scripture,
        on_delete=models.CASCADE,
        verbose_name=_("所属经训"),
        related_name='chapters'
    )
    title = models.CharField(_("章节标题"), max_length=200)
    content = models.TextField(_("章节内容"))
    order = models.PositiveIntegerField(_("排序"), default=0)

    class Meta:
        verbose_name = _("经训章节")
        verbose_name_plural = _("经训章节")
        db_table = 'articles_scripture_chapter'
        ordering = ['scripture', 'order']
        indexes = [
            models.Index(fields=['scripture', 'order']),
        ]

    def __str__(self):
        return f"{self.scripture.title} - {self.title}"


# ==================== 联系我们 (无媒体字段) ====================

class Contact(TimeStampedModel):
    """联系我们"""
    email = models.EmailField(_("邮箱"))
    subject = models.CharField(_("主题"), max_length=255)
    message = models.TextField(_("内容"))
    is_handled = models.BooleanField(_("是否已处理"), default=False)

    class Meta:
        verbose_name = _("联系我们")
        verbose_name_plural = _("联系我们")
        db_table = 'articles_contact'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.subject}"