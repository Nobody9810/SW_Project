import os
import sys
import django
from django.db import transaction
from datetime import datetime


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connections
def get_old_data(table_name, db='old_db'):
    """从旧数据库获取数据"""
    with connections[db].cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table_name}`")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]


def safe_get(item, key, default=None):
    """安全获取字典值"""
    value = item.get(key, default)
    if value is None:
        return default
    return value


def migrate_news():
    """迁移通讯数据"""
    from articles.models import News
    
    print("开始迁移通讯数据...")
    old_data = get_old_data('home_通讯')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                News.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    source=safe_get(item, '资源', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条通讯数据")
    return success


def migrate_book_info():
    """迁移书讯数据"""
    from articles.models import BookInfo
    
    print("开始迁移书讯数据...")
    old_data = get_old_data('home_书讯')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                BookInfo.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    author_intro=safe_get(item, '作者简介', ''),
                    catalog=safe_get(item, '目录', ''),
                    preface=safe_get(item, '前言', ''),
                    isbn=safe_get(item, 'ISBN', ''),
                    publisher=safe_get(item, '出版社', ''),
                    publish_date=safe_get(item, '出版年'),
                    price=safe_get(item, '定价', ''),
                    pages=safe_get(item, '页数'),
                    binding=safe_get(item, '装帧', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条书讯数据")
    return success


def migrate_book_reviews():
    """迁移书评数据"""
    from articles.models import BookReview, BookReviewCategory
    
    # 先迁移分类
    print("开始迁移书评分类...")
    old_categories = get_old_data('home_书评_分类')
    
    category_success = 0
    with transaction.atomic():
        for cat in old_categories:
            try:
                BookReviewCategory.objects.create(
                    id=cat['id'],
                    name=safe_get(cat, '名称', ''),
                    slug=safe_get(cat, '名称', '').lower().replace(' ', '-'),
                    description=''
                )
                category_success += 1
            except Exception as e:
                print(f"  ✗ 分类 ID {cat['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {category_success}/{len(old_categories)} 个书评分类")
    
    # 迁移书评
    print("开始迁移书评数据...")
    old_data = get_old_data('home_书评')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                BookReview.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    source=safe_get(item, '出处', ''),
                    book_publish_date=safe_get(item, '书籍出版日期'),
                    category_id=safe_get(item, '分类_id'),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条书评数据")
    return success


def migrate_opinions():
    """迁移观点数据"""
    from articles.models import Opinion
    
    print("开始迁移观点数据...")
    old_data = get_old_data('home_观点')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                Opinion.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    source=safe_get(item, '出处', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条观点数据")
    return success


def migrate_literature():
    """迁移文艺数据"""
    from articles.models import Literature
    
    print("开始迁移文艺数据...")
    old_data = get_old_data('home_文艺')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                Literature.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    source=safe_get(item, '出处', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条文艺数据")
    return success


def migrate_qa():
    """迁移问答数据"""
    from articles.models import QA
    
    print("开始迁移问答数据...")
    old_data = get_old_data('home_问答')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                QA.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    is_approved=safe_get(item, '通过', False),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date())
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条问答数据")
    return success


def migrate_translations():
    """迁移译林数据"""
    from articles.models import Translation
    
    print("开始迁移译林数据...")
    old_data = get_old_data('home_译林')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                Translation.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    original_title=safe_get(item, '原文标题', ''),
                    original_author=safe_get(item, '原文作者', ''),
                    original_publish_date=safe_get(item, '原文出版日期'),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条译林数据")
    return success


def migrate_history():
    """迁移文史数据"""
    from articles.models import History
    
    print("开始迁移文史数据...")
    old_data = get_old_data('home_文史')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                History.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    source=safe_get(item, '资源', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条文史数据")
    return success


def migrate_papers():
    """迁移论文数据"""
    from articles.models import Paper
    
    print("开始迁移论文数据...")
    old_data = get_old_data('home_论文')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                Paper.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    author=safe_get(item, '作者', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', ''),
                    document=safe_get(item, '文档', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条论文数据")
    return success


def migrate_classic_books():
    """迁移古籍数据"""
    from articles.models import ClassicBook
    
    print("开始迁移古籍数据...")
    old_data = get_old_data('home_古籍')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                ClassicBook.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    author=safe_get(item, '作者', ''),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    document=safe_get(item, '文档', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条古籍数据")
    return success


def migrate_library():
    """迁移书库数据"""
    from articles.models import Library
    
    print("开始迁移书库数据...")
    old_data = get_old_data('home_书库')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                Library.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    content=safe_get(item, '内容', ''),
                    author=safe_get(item, '作者', ''),
                    author_intro=safe_get(item, '作者简介', ''),
                    content_intro=safe_get(item, '内容简介', ''),
                    isbn=safe_get(item, 'ISBN', ''),
                    publish_date=safe_get(item, '出版日期'),
                    is_published=safe_get(item, '发布状态', False),
                    total_views=safe_get(item, '总浏览量', 0),
                    today_views=safe_get(item, '今日浏览量', 0),
                    likes=safe_get(item, 'likes', 0),
                    dislikes=safe_get(item, 'dislikes', 0),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    last_view_date=safe_get(item, '最后统计日期', datetime.now().date()),
                    image=safe_get(item, '图片', ''),
                    document=safe_get(item, '文档', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条书库数据")
    return success


def migrate_scriptures():
    """迁移经训数据"""
    from articles.models import Scripture, ScriptureChapter
    
    print("开始迁移经训数据...")
    old_scriptures = get_old_data('home_经训')
    
    success = 0
    with transaction.atomic():
        for item in old_scriptures:
            try:
                Scripture.objects.create(
                    id=item['id'],
                    title=safe_get(item, '标题', ''),
                    is_published=safe_get(item, '发布状态', False),
                    created_at=safe_get(item, '更新时间', datetime.now()),
                    updated_at=safe_get(item, '更新时间', datetime.now()),
                    image=safe_get(item, '图片', '')
                )
                success += 1
            except Exception as e:
                print(f"  ✗ 经训 ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_scriptures)} 条经训数据")
    
    print("开始迁移经训章节数据...")
    old_chapters = get_old_data('home_章节_经训')
    
    chapter_success = 0
    with transaction.atomic():
        for idx, item in enumerate(old_chapters):
            try:
                ScriptureChapter.objects.create(
                    id=item['id'],
                    scripture_id=item['经训_id'],
                    title=safe_get(item, '章节', ''),
                    content=safe_get(item, '内容', ''),
                    is_published=safe_get(item, '发布状态', False),
                    order=idx,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                chapter_success += 1
            except Exception as e:
                print(f"  ✗ 章节 ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {chapter_success}/{len(old_chapters)} 条经训章节数据")
    return success + chapter_success


def migrate_contacts():
    """迁移联系我们数据"""
    from articles.models import Contact
    
    print("开始迁移联系我们数据...")
    old_data = get_old_data('home_contact')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                Contact.objects.create(
                    id=item['id'],
                    email=safe_get(item, '邮箱', ''),
                    subject=safe_get(item, '主题', ''),
                    message=safe_get(item, '内容', ''),
                    created_at=datetime.now()
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条联系我们数据")
    return success


def migrate_reactions():
    """迁移用户反应数据"""
    from reactions.models import UserReaction
    
    print("开始迁移用户反应数据...")
    old_data = get_old_data('home_userreaction')
    
    success = 0
    with transaction.atomic():
        for item in old_data:
            try:
                UserReaction.objects.create(
                    id=item['id'],
                    user_session=item['user_session'],
                    reaction_type=item['reaction_type'],
                    content_type_id=item['content_type_id'],
                    object_id=item['object_id'],
                    created_at=item['created_at']
                )
                success += 1
            except Exception as e:
                print(f"  ✗ ID {item['id']} 失败: {str(e)}")
    
    print(f"✓ 成功迁移 {success}/{len(old_data)} 条反应数据")
    return success


def main():
    """主函数"""
    print("=" * 70)
    print("数据迁移: shuwei → shuwei_dev")
    print("=" * 70)
    
    migrations = [
        ('通讯', migrate_news),
        ('书讯', migrate_book_info),
        ('书评', migrate_book_reviews),
        ('观点', migrate_opinions),
        ('文艺', migrate_literature),
        ('问答', migrate_qa),
        ('译林', migrate_translations),
        ('文史', migrate_history),
        ('论文', migrate_papers),
        ('古籍', migrate_classic_books),
        ('书库', migrate_library),
        ('经训', migrate_scriptures),
        ('联系我们', migrate_contacts),
        ('用户反应', migrate_reactions),
    ]
    
    total_migrated = 0
    failed = []
    
    for name, func in migrations:
        print(f"\n{'='*70}")
        try:
            count = func()
            total_migrated += count
        except Exception as e:
            print(f"\n✗ {name} 迁移失败: {str(e)}")
            import traceback
            traceback.print_exc()
            failed.append(name)
            
            response = input(f"\n是否继续迁移其他数据？(yes/no): ")
            if response.lower() != 'yes':
                break
    
    print("\n" + "=" * 70)
    print("迁移完成总结")
    print("=" * 70)
    print(f"总共成功迁移: {total_migrated} 条记录")
    
    if failed:
        print(f"\n失败的迁移: {', '.join(failed)}")
    else:
        print("\n✓ 所有数据迁移成功！")
    
    print("=" * 70)


if __name__ == '__main__':
    response = input("\n⚠️  警告：此操作将迁移所有数据到 shuwei_dev。是否继续？(yes/no): ")
    if response.lower() == 'yes':
        main()
    else:
        print("已取消迁移")