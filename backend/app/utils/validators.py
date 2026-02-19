from typing import Iterable
from backend.app.utils.constants import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE

def _get_ext(filename: str) -> str:
    if "." not in filename:
        raise ValueError("invalid file name")
    return filename.rsplit(".", 1)[1].lower()

def validate_cv_filename(filename: str, allowed: Iterable[str] = ALLOWED_EXTENSIONS) -> str:
    """Return filename if extension allowed, else raise ValueError."""
    ext = _get_ext(filename)
    if ext not in allowed:
        raise ValueError(f"invalid file extension: .{ext}")
    return filename

def validate_cv_size(size: int, max_size: int = MAX_UPLOAD_SIZE) -> int:
    """Return size if within limits, else raise ValueError."""
    if not isinstance(size, int) or size < 0:
        raise ValueError("file size must be a non-negative integer")
    if size > max_size:
        raise ValueError(f"file too large (max {max_size} bytes)")
    return size
