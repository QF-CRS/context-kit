"""Safe, deterministic context bundles for software repositories."""

from .model import FileRecord, PackOptions, PackResult, build_pack

__all__ = ["FileRecord", "PackOptions", "PackResult", "build_pack"]

__version__ = "0.1.0"
