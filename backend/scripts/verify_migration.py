import os
import sys
import django




from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from articles.models import *
from reactions.models import UserReaction

models_to_check = [
    ('通讯', News),
    ('书讯', BookInfo),
    ('书评', BookReview),
    ('观点', Opinion),
    ('文艺', Literature),
    ('问答', QA),
    ('译林', Translation),
    ('文史', History),
    ('论文', Paper),
    ('古籍', ClassicBook),
    ('书库', Library),
    ('经训', Scripture),
    ('经训章节', ScriptureChapter),
    ('用户反应', UserReaction),
]

print("=" * 60)
print("数据迁移验证")
print("=" * 60)

for name, model in models_to_check:
    count = model.objects.count()
    status = "✓" if count > 0 else "✗"
    print(f"{status} {name:12s}: {count:5d} 条记录")

print("=" * 60)
