"""
ui/detail_panel.py
Side panel that displays full post detail including comments.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QScrollArea, QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from database.models import Post, Comment


class SectionLabel(QLabel):
    def __init__(self, text: str, parent=None):
        super().__init__(text.upper(), parent)
        self.setStyleSheet(
            "color: #6B7280; font-size: 10px; font-weight: 700; letter-spacing: 2px;"
            " margin-top: 12px; margin-bottom: 4px;"
        )


class ValueLabel(QLabel):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.setStyleSheet("color: #D1D5DB; font-size: 13px;")
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)


class Divider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet("color: #262626; margin: 8px 0;")


class CommentCard(QWidget):
    def __init__(self, comment: Comment, parent=None):
        super().__init__(parent)
        self.setObjectName("comment_card")
        self.setStyleSheet("""
            QWidget#comment_card {
                background-color: #1C1C1C;
                border: 1px solid #2A2A2A;
                border-left: 3px solid #F59E0B;
                border-radius: 6px;
                padding: 0;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        author = QLabel(f"✎ {comment.author}")
        author.setStyleSheet("color: #F59E0B; font-size: 12px; font-weight: 700;")

        body = QLabel(comment.body)
        body.setWordWrap(True)
        body.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        body.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(author)
        layout.addWidget(body)


class DetailPanel(QWidget):
    """Right-side panel showing post detail and comments."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("detail_panel")
        self.setStyleSheet("""
            QWidget#detail_panel {
                background-color: #181818;
                border: 1px solid #262626;
                border-radius: 8px;
            }
        """)
        self.setMinimumWidth(300)
        self._setup_ui()
        self._show_placeholder()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel header
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet(
            "background-color: #1A1A1A; border-bottom: 1px solid #262626;"
            " border-top-left-radius: 8px; border-top-right-radius: 8px;"
        )
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 0, 16, 0)

        icon = QLabel("◈")
        icon.setStyleSheet("color: #F59E0B; font-size: 16px;")

        title = QLabel("Detail Post")
        title.setStyleSheet("color: #E8E8E8; font-size: 13px; font-weight: 700; letter-spacing: 0.5px;")

        h_layout.addWidget(icon)
        h_layout.addWidget(title)
        h_layout.addStretch()

        main_layout.addWidget(header)

        # Scrollable content
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background-color: #181818;")

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #181818;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(4)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll, 1)

    def _clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_placeholder(self):
        self._clear_content()
        placeholder = QLabel("← Pilih post dari tabel\nuntuk melihat detail")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(
            "color: #374151; font-size: 14px; padding: 40px 20px;"
        )
        self.content_layout.addWidget(placeholder)

    def show_loading(self):
        self._clear_content()
        loading = QLabel("⏳  Memuat detail...")
        loading.setAlignment(Qt.AlignCenter)
        loading.setStyleSheet("color: #F59E0B; font-size: 13px; padding: 40px 20px;")
        self.content_layout.addWidget(loading)

    def show_post(self, post: Post):
        self._clear_content()

        # Title
        title_label = QLabel(post.title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet(
            "color: #F59E0B; font-size: 16px; font-weight: 700; line-height: 1.3;"
        )
        title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.content_layout.addWidget(title_label)

        # Status badge
        badge_container = QWidget()
        badge_layout = QHBoxLayout(badge_container)
        badge_layout.setContentsMargins(0, 4, 0, 0)
        badge_layout.setSpacing(0)

        status_color = "#4ADE80" if post.status == "published" else "#A8A29E"
        status_bg = "#052E16" if post.status == "published" else "#1C1917"
        status_border = "#166534" if post.status == "published" else "#44403C"

        badge = QLabel(f"  {'●' if post.status == 'published' else '○'}  {post.status.upper()}  ")
        badge.setStyleSheet(f"""
            background-color: {status_bg};
            color: {status_color};
            border: 1px solid {status_border};
            border-radius: 10px;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
        """)
        badge_layout.addWidget(badge)
        badge_layout.addStretch()
        self.content_layout.addWidget(badge_container)

        self.content_layout.addWidget(Divider())

        # ID
        self.content_layout.addWidget(SectionLabel("ID"))
        self.content_layout.addWidget(ValueLabel(str(post.id)))

        # Author
        self.content_layout.addWidget(SectionLabel("Penulis"))
        self.content_layout.addWidget(ValueLabel(post.author))

        # Slug
        self.content_layout.addWidget(SectionLabel("Slug"))
        slug_lbl = ValueLabel(post.slug)
        slug_lbl.setStyleSheet("color: #60A5FA; font-size: 12px; font-family: monospace;")
        self.content_layout.addWidget(slug_lbl)

        # Body
        self.content_layout.addWidget(Divider())
        self.content_layout.addWidget(SectionLabel("Konten"))
        body_label = ValueLabel(post.body)
        body_label.setStyleSheet(
            "color: #9CA3AF; font-size: 12px; line-height: 1.6;"
        )
        self.content_layout.addWidget(body_label)

        # Comments
        self.content_layout.addWidget(Divider())
        comment_count = len(post.comments)
        comment_header = SectionLabel(f"Komentar ({comment_count})")
        self.content_layout.addWidget(comment_header)

        if comment_count == 0:
            no_comment = QLabel("Belum ada komentar.")
            no_comment.setStyleSheet("color: #4B5563; font-size: 12px; font-style: italic; padding: 4px 0;")
            self.content_layout.addWidget(no_comment)
        else:
            for comment in post.comments:
                card = CommentCard(comment)
                self.content_layout.addWidget(card)

        self.content_layout.addStretch()

    def show_error(self, message: str):
        self._clear_content()
        error_label = QLabel(f"⚠ {message}")
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("color: #F87171; font-size: 13px; padding: 40px 16px;")
        self.content_layout.addWidget(error_label)

    def reset(self):
        self._show_placeholder()
