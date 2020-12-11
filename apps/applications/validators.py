from pathlib import Path

from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = Path(value.name).suffix
    valid_extensions = ['.pdf', '.docx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Расширение файла не поддерживается. \nЗагрузите файл в одном из форматов : .xls ; .docx ; .pdf.')
