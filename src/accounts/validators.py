from django.core.exceptions import ValidationError

def validate_avatar(img):
    img_size = img.size
    max_upload_size = 1200000 # 1.2 MB
    if img_size > max_upload_size:
        raise ValidationError('حجم تصویر باید کمتر از 1.2 مگابایت باشد.')