"""
database/models.py
Data models for Post Manager application.
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Comment:
    """Represents a comment on a post."""
    id: int
    post_id: int
    author: str
    body: str

    @classmethod
    def from_dict(cls, data: dict) -> "Comment":
        return cls(
            id=data.get("id", 0),
            post_id=data.get("post_id", 0),
            author=data.get("author", ""),
            body=data.get("body", ""),
        )


@dataclass
class Post:
    """Represents a blog post."""
    id: int
    title: str
    body: str
    author: str
    slug: str
    status: str
    comments: List[Comment] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Post":
        comments_data = data.get("comments", [])
        comments = [Comment.from_dict(c) for c in comments_data]
        return cls(
            id=data.get("id", 0),
            title=data.get("title", ""),
            body=data.get("body", ""),
            author=data.get("author", ""),
            slug=data.get("slug", ""),
            status=data.get("status", "draft"),
            comments=comments,
        )

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "body": self.body,
            "author": self.author,
            "slug": self.slug,
            "status": self.status,
        }


@dataclass
class ApiResponse:
    """Wrapper for API responses."""
    success: bool
    data: Optional[any] = None
    error_message: str = ""
    status_code: int = 0
    validation_errors: dict = field(default_factory=dict)
