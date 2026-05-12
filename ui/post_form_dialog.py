"""
ui/post_form_dialog.py
Dialog for creating and editing posts.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QComboBox, QPushButton,
    QFrame, QWidget, QScrollArea, QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from database.models import Post


class FieldGroup(QWidget):
    """Label + input widget pair."""

    def __init__(self, label: str, widget, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        lbl = QLabel(label.upper())
        lbl.setStyleSheet("color: #4A5586; font-size: 11px; font-weight: 700; letter-spacing: 1.5px;")
        layout.addWidget(lbl)
        layout.addWidget(widget)


class PostFormDialog(QDialog):
    """Modal dialog for Add / Edit post."""

    submitted = Signal(dict)

    def __init__(self, parent=None, post: Post = None):
        super().__init__(parent)
        self.post = post
        self.is_edit = post is not None
        self._setup_ui()
        if self.is_edit:
            self._populate(post)

    def _setup_ui(self):
        self.setWindowTitle("Edit Post" if self.is_edit else "Tambah Post Baru")
        self.setMinimumWidth(520)
        self.setMinimumHeight(560)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog { background-color: #12152B; border: 1px solid #2D3158; }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ──
        header = QWidget()
        header.setStyleSheet("background-color: #0D0F1A; border-bottom: 2px solid #7C3AED;")
        header.setFixedHeight(64)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(24, 0, 24, 0)

        icon_label = QLabel("✦")
        icon_label.setStyleSheet("color: #7C3AED; font-size: 20px;")

        title_label = QLabel("Edit Post" if self.is_edit else "Tambah Post Baru")
        title_label.setStyleSheet("color: #A78BFA; font-size: 16px; font-weight: 700; letter-spacing: 1px;")

        h_layout.addWidget(icon_label)
        h_layout.addWidget(title_label)
        h_layout.addStretch()
        root.addWidget(header)

        # ── Scrollable body ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        body = QWidget()
        body.setStyleSheet("background-color: #12152B;")
        form = QVBoxLayout(body)
        form.setContentsMargins(24, 20, 24, 20)
        form.setSpacing(16)

        # Title
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Judul post...")
        self.input_title.setMinimumHeight(40)
        form.addWidget(FieldGroup("Judul *", self.input_title))

        # Author
        self.input_author = QLineEdit()
        self.input_author.setPlaceholderText("Nama penulis...")
        self.input_author.setMinimumHeight(40)
        form.addWidget(FieldGroup("Penulis *", self.input_author))

        # Slug
        self.input_slug = QLineEdit()
        self.input_slug.setPlaceholderText("url-friendly-identifier (contoh: judul-post)")
        self.input_slug.setMinimumHeight(40)
        slug_group = QWidget()
        slug_layout = QVBoxLayout(slug_group)
        slug_layout.setContentsMargins(0, 0, 0, 0)
        slug_layout.setSpacing(4)
        slug_lbl = QLabel("SLUG * (harus unik)")
        slug_lbl.setStyleSheet("color: #4A5586; font-size: 11px; font-weight: 700; letter-spacing: 1.5px;")
        self.slug_hint = QLabel("Hanya huruf kecil, angka, dan tanda hubung (-)")
        self.slug_hint.setStyleSheet("color: #2D3158; font-size: 10px; font-style: italic;")
        slug_layout.addWidget(slug_lbl)
        slug_layout.addWidget(self.input_slug)
        slug_layout.addWidget(self.slug_hint)
        form.addWidget(slug_group)

        # Status
        self.combo_status = QComboBox()
        self.combo_status.addItem("published")
        self.combo_status.addItem("draft")
        self.combo_status.setMinimumHeight(40)
        form.addWidget(FieldGroup("Status *", self.combo_status))

        # Body
        self.input_body = QTextEdit()
        self.input_body.setPlaceholderText("Tulis isi konten post di sini...")
        self.input_body.setMinimumHeight(150)
        form.addWidget(FieldGroup("Konten *", self.input_body))

        # Validation error box
        self.error_container = QWidget()
        self.error_container.setObjectName("error_box")
        self.error_container.hide()
        err_layout = QVBoxLayout(self.error_container)
        err_layout.setContentsMargins(10, 8, 10, 8)
        err_layout.setSpacing(2)
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #FCA5A5; font-size: 12px;")
        err_layout.addWidget(self.error_label)
        form.addWidget(self.error_container)

        form.addStretch()
        scroll.setWidget(body)
        root.addWidget(scroll, 1)

        # ── Footer buttons ──
        footer = QWidget()
        footer.setStyleSheet("background-color: #0D0F1A; border-top: 1px solid #1E2240;")
        footer.setFixedHeight(64)
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(24, 0, 24, 0)
        f_layout.setSpacing(12)

        f_layout.addStretch()

        self.btn_cancel = QPushButton("Batal")
        self.btn_cancel.setFixedSize(100, 38)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_submit = QPushButton("Simpan" if self.is_edit else "Tambah Post")
        self.btn_submit.setObjectName("btn_add")
        self.btn_submit.setFixedHeight(38)
        self.btn_submit.setMinimumWidth(130)
        self.btn_submit.clicked.connect(self._on_submit)

        f_layout.addWidget(self.btn_cancel)
        f_layout.addWidget(self.btn_submit)
        root.addWidget(footer)

        # Auto-slug generation
        self.input_title.textChanged.connect(self._auto_slug)

    def _auto_slug(self, text: str):
        """Auto-generate slug from title when not in edit mode."""
        if not self.is_edit and not self.input_slug.hasFocus():
            slug = text.lower().strip()
            slug = "".join(c if c.isalnum() or c in "-_ " else "" for c in slug)
            slug = slug.replace(" ", "-").replace("_", "-")
            while "--" in slug:
                slug = slug.replace("--", "-")
            slug = slug.strip("-")
            self.input_slug.setText(slug)

    def _populate(self, post: Post):
        """Fill form fields with existing post data."""
        self.input_title.setText(post.title)
        self.input_author.setText(post.author)
        self.input_slug.setText(post.slug)
        idx = self.combo_status.findText(post.status)
        if idx >= 0:
            self.combo_status.setCurrentIndex(idx)
        self.input_body.setPlainText(post.body)

    def _on_submit(self):
        """Validate and emit submitted signal."""
        self.hide_error()

        title = self.input_title.text().strip()
        author = self.input_author.text().strip()
        slug = self.input_slug.text().strip()
        status = self.combo_status.currentText()
        body = self.input_body.toPlainText().strip()

        errors = []
        if not title:
            errors.append("• Judul tidak boleh kosong.")
        if not author:
            errors.append("• Nama penulis tidak boleh kosong.")
        if not slug:
            errors.append("• Slug tidak boleh kosong.")
        if not body:
            errors.append("• Konten tidak boleh kosong.")

        if errors:
            self.show_error("\n".join(errors))
            return

        payload = {
            "title": title,
            "author": author,
            "slug": slug,
            "status": status,
            "body": body,
        }
        self.submitted.emit(payload)

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_container.show()

    def hide_error(self):
        self.error_container.hide()

    def set_loading(self, loading: bool):
        self.btn_submit.setEnabled(not loading)
        self.btn_cancel.setEnabled(not loading)
        if loading:
            self.btn_submit.setText("Menyimpan...")
        else:
            self.btn_submit.setText("Simpan" if self.is_edit else "Tambah Post")