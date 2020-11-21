from pathlib import Path

from django.core.exceptions import ValidationError

#валидация отчетностей
def validate_file_extension(value):
    ext = Path(value.name).suffix
    valid_extensions = ['.pdf', '.docx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
