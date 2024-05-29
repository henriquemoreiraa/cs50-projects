import magic
from django.core.exceptions import ValidationError


def validate_audio_file(file):
    # Define allowed MIME types for audio files
    allowed_mime_types = [
        "audio/mpeg",  # .mp3
        "audio/x-wav",  # .wav
        "audio/ogg",  # .ogg
        "audio/flac",  # .flac
        "audio/mp4",  # .m4a
        "audio/x-aiff",  # .aiff
        "audio/aac",  # .aac
    ]

    # Use python-magic to determine the file's MIME type
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read())
    file.seek(0)  # Reset file pointer to the beginning after reading

    # Check if the file's MIME type is in the allowed list
    if file_mime_type not in allowed_mime_types:
        raise ValidationError(
            f"Unsupported file type: {file_mime_type}. Please upload an audio file."
        )
