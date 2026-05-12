"""
logic/workers.py
QThread workers — all network requests run here, never on the UI thread.
"""

from PySide6.QtCore import QThread, Signal
from logic.api_client import PostApiClient
from database.models import ApiResponse


class BaseWorker(QThread):
    """Base worker with finished signal."""
    finished = Signal(object)  # emits ApiResponse

    def __init__(self):
        super().__init__()
        self.client = PostApiClient()


class FetchPostsWorker(BaseWorker):
    """Worker: GET all posts."""

    def run(self):
        result = self.client.get_all_posts()
        self.finished.emit(result)


class FetchPostDetailWorker(BaseWorker):
    """Worker: GET single post with comments."""

    def __init__(self, post_id: int):
        super().__init__()
        self.post_id = post_id

    def run(self):
        result = self.client.get_post(self.post_id)
        self.finished.emit(result)


class CreatePostWorker(BaseWorker):
    """Worker: POST new post."""

    def __init__(self, payload: dict):
        super().__init__()
        self.payload = payload

    def run(self):
        result = self.client.create_post(self.payload)
        self.finished.emit(result)


class UpdatePostWorker(BaseWorker):
    """Worker: PUT update post."""

    def __init__(self, post_id: int, payload: dict):
        super().__init__()
        self.post_id = post_id
        self.payload = payload

    def run(self):
        result = self.client.update_post(self.post_id, self.payload)
        self.finished.emit(result)


class DeletePostWorker(BaseWorker):
    """Worker: DELETE post."""

    def __init__(self, post_id: int):
        super().__init__()
        self.post_id = post_id

    def run(self):
        result = self.client.delete_post(self.post_id)
        self.finished.emit(result)
