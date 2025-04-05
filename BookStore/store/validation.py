from django.core.exceptions import ValidationError
from PIL import Image


def validate_cover_image_size(image):
    max_width = 400  # Max width in pixels
    max_height = 600  # Max height in pixels

    img = Image.open(image)
    if img.width != max_width or img.height != max_height:
        raise ValidationError(f"Image size must be at most {max_width}x{max_height} pixels.")
    
def validate_image_file_size(image):
    max_size_kb = 2048  # 2MB (in KB)
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"Image file size cannot exceed {max_size_kb}KB.")
    
def validate_author_image_size(image):
    max_width = 400  # Max width in pixels
    max_height = 400  # Max height in pixels

    img = Image.open(image)
    if img.width != max_width or img.height != max_height:
        raise ValidationError(f"Image size must be at most {max_width}x{max_height} pixels.")