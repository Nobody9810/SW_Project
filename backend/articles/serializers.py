"""
完整的 Serializers
为所有模型提供序列化支持
"""

from rest_framework import serializers

from .models import (
    News, BookInfo, BookReview, BookReviewCategory,
    Opinion, Literature, QA, Translation, History,
    Paper, ClassicBook, Library, Scripture, ScriptureChapter,
    Contact
)


# ==================== 基础 Serializers ====================

class BaseArticleSerializer(serializers.ModelSerializer):
    """文章基础序列化器"""
    
    class Meta:
        fields = [
            'id', 'title', 'content', 'author', 'source',
            'is_published', 'total_views', 'today_views',
            'likes', 'dislikes', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]


class BaseArticleListSerializer(serializers.ModelSerializer):
    """列表视图的简化序列化器"""
    
    class Meta:
        fields = [
            'id', 'title', 'author', 'total_views',
            'likes', 'updated_at'
        ]


# ==================== 通讯 ====================

class NewsSerializer(BaseArticleSerializer):
    """通讯详情序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = News
        fields = BaseArticleSerializer.Meta.fields + ['image', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class NewsListSerializer(BaseArticleListSerializer):
    """通讯列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = News
        fields = BaseArticleListSerializer.Meta.fields + ['image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 书讯 ====================

class BookInfoSerializer(BaseArticleSerializer):
    """书讯详情序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = BookInfo
        fields = BaseArticleSerializer.Meta.fields + [
            'author_intro', 'catalog', 'preface', 'isbn',
            'publisher', 'publish_date', 'price', 'pages',
            'binding', 'image', 'image_url'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class BookInfoListSerializer(BaseArticleListSerializer):
    """书讯列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = BookInfo
        fields = BaseArticleListSerializer.Meta.fields + ['image_url', 'publisher']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 书评分类 ====================

class BookReviewCategorySerializer(serializers.ModelSerializer):
    """书评分类序列化器"""
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BookReviewCategory
        fields = ['id', 'name', 'slug', 'description', 'review_count']
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_published=True).count()


# ==================== 书评 ====================

class BookReviewSerializer(BaseArticleSerializer):
    """书评详情序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = BookReview
        fields = BaseArticleSerializer.Meta.fields + [
            'book_publish_date', 'image', 'image_url',
            'category', 'category_name'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class BookReviewListSerializer(BaseArticleListSerializer):
    """书评列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = BookReview
        fields = BaseArticleListSerializer.Meta.fields + ['image_url', 'category_name']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 观点 ====================

class OpinionSerializer(BaseArticleSerializer):
    """观点序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = Opinion
        fields = BaseArticleSerializer.Meta.fields + ['image', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class OpinionListSerializer(BaseArticleListSerializer):
    """观点列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = Opinion
        fields = BaseArticleListSerializer.Meta.fields + ['image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 文艺 ====================

class LiteratureSerializer(BaseArticleSerializer):
    """文艺序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = Literature
        fields = BaseArticleSerializer.Meta.fields + ['image', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class LiteratureListSerializer(BaseArticleListSerializer):
    """文艺列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = Literature
        fields = BaseArticleListSerializer.Meta.fields + ['image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 问答 ====================

class QASerializer(BaseArticleSerializer):
    """问答序列化器"""
    
    class Meta(BaseArticleSerializer.Meta):
        model = QA
        # QA 没有 author 字段
        fields = [f for f in BaseArticleSerializer.Meta.fields if f != 'author'] + ['is_approved']


class QAListSerializer(BaseArticleListSerializer):
    """问答列表序列化器"""
    
    class Meta(BaseArticleListSerializer.Meta):
        model = QA
        fields = [f for f in BaseArticleListSerializer.Meta.fields if f != 'author']


# ==================== 译林 ====================

class TranslationSerializer(BaseArticleSerializer):
    """译林序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = Translation
        fields = BaseArticleSerializer.Meta.fields + [
            'original_title', 'original_author', 'original_publish_date',
            'image', 'image_url'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class TranslationListSerializer(BaseArticleListSerializer):
    """译林列表序列化器"""
    original_title = serializers.CharField()
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = Translation
        fields = BaseArticleListSerializer.Meta.fields + ['original_title', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 文史 ====================

class HistorySerializer(BaseArticleSerializer):
    """文史序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleSerializer.Meta):
        model = History
        fields = BaseArticleSerializer.Meta.fields + ['image', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class HistoryListSerializer(BaseArticleListSerializer):
    """文史列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta(BaseArticleListSerializer.Meta):
        model = History
        fields = BaseArticleListSerializer.Meta.fields + ['image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 论文 ====================

class PaperSerializer(serializers.ModelSerializer):
    """论文序列化器"""
    image_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Paper
        fields = [
            'id', 'title', 'author', 'source', 'image', 'image_url',
            'document', 'document_url', 'is_published',
            'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_document_url(self, obj):
        if obj.document:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.document.url)
        return None


class PaperListSerializer(serializers.ModelSerializer):
    """论文列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Paper
        fields = ['id', 'title', 'author', 'image_url', 'total_views', 'likes', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 古籍 ====================

class ClassicBookSerializer(serializers.ModelSerializer):
    """古籍序列化器"""
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassicBook
        fields = [
            'id', 'title', 'author', 'source', 'document', 'document_url',
            'is_published', 'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]
    
    def get_document_url(self, obj):
        if obj.document:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.document.url)
        return None


class ClassicBookListSerializer(serializers.ModelSerializer):
    """古籍列表序列化器"""
    
    class Meta:
        model = ClassicBook
        fields = ['id', 'title', 'author', 'total_views', 'likes', 'updated_at']


# ==================== 书库 ====================

class LibrarySerializer(serializers.ModelSerializer):
    """书库序列化器"""
    image_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Library
        fields = [
            'id', 'title', 'author', 'author_intro', 'content_intro',
            'publish_date', 'isbn', 'image', 'image_url',
            'document', 'document_url', 'is_published',
            'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'total_views', 'today_views', 'likes', 'dislikes',
            'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_document_url(self, obj):
        if obj.document:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.document.url)
        return None


class LibraryListSerializer(serializers.ModelSerializer):
    """书库列表序列化器"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Library
        fields = ['id', 'title', 'author', 'image_url', 'total_views', 'likes', 'updated_at']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 经训 ====================

class ScriptureChapterSerializer(serializers.ModelSerializer):
    """经训章节序列化器"""
    
    class Meta:
        model = ScriptureChapter
        fields = ['id', 'title', 'content', 'order', 'is_published', 'created_at', 'updated_at']


class ScriptureSerializer(serializers.ModelSerializer):
    """经训序列化器"""
    chapters = ScriptureChapterSerializer(many=True, read_only=True)
    chapter_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Scripture
        fields = [
            'id', 'title', 'image', 'image_url',
            'is_published', 'chapter_count', 'chapters',
            'created_at', 'updated_at'
        ]
    
    def get_chapter_count(self, obj):
        return obj.chapters.filter(is_published=True).count()
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class ScriptureListSerializer(serializers.ModelSerializer):
    """经训列表序列化器"""
    chapter_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Scripture
        fields = ['id', 'title', 'image_url', 'chapter_count', 'updated_at']
    
    def get_chapter_count(self, obj):
        return obj.chapters.filter(is_published=True).count()
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


# ==================== 联系我们 ====================

class ContactSerializer(serializers.ModelSerializer):
    """联系我们序列化器"""
    
    class Meta:
        model = Contact
        fields = ['id', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['created_at']