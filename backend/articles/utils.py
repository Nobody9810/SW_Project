# articles/utils.py

import sys
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from pypdf import PdfReader, PdfWriter

def compress_image(image_field, max_width=1200, quality=75):
    """
    图片压缩：调整尺寸 + 转换为 JPEG + 降低质量
    """
    # 1. 空值或非上传对象检查
    if not image_field or not hasattr(image_field, 'file'):
        return image_field
        
    # 避免对已经存在的 ImageFieldFile (非新上传的) 重复压缩
    # InMemoryUploadedFile 是新上传文件的特征
    if not isinstance(image_field.file, InMemoryUploadedFile):
        return image_field

    try:
        img = Image.open(image_field)
        
        # 自动旋转（处理手机拍摄的照片方向）
        img = ImageOps.exif_transpose(img)

        # 转换为 RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # 调整尺寸
        if img.width > max_width:
            output_size = (max_width, int(img.height * max_width / img.width))
            img.thumbnail(output_size, Image.Resampling.LANCZOS)

        output_io = BytesIO()
        img.save(output_io, format='JPEG', quality=quality, optimize=True)
        output_io.seek(0)

        return InMemoryUploadedFile(
            output_io,
            'ImageField',
            f"{image_field.name.split('.')[0]}.jpg",
            'image/jpeg',
            sys.getsizeof(output_io),
            None
        )
    except Exception as e:
        print(f"Image compression failed: {e}")
        return image_field

def compress_pdf(file_field):
    """
    PDF 压缩：去除多余元数据，压缩内容流 (Lossless)
    """
    if not file_field or not hasattr(file_field, 'file'):
        return file_field
        
    if not isinstance(file_field.file, InMemoryUploadedFile):
        return file_field

    try:
        reader = PdfReader(file_field)
        writer = PdfWriter()

        # 复制所有页面并应用压缩
        for page in reader.pages:
            page.compress_content_streams()  # 关键步骤：压缩流
            writer.add_page(page)

        # 去除元数据以减小体积
        writer.add_metadata({})

        output_io = BytesIO()
        writer.write(output_io)
        output_io.seek(0)

        return InMemoryUploadedFile(
            output_io,
            'FileField',
            file_field.name,
            'application/pdf',
            sys.getsizeof(output_io),
            None
        )
    except Exception as e:
        print(f"PDF compression failed: {e}")
        return file_field