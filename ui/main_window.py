"""
ui/main_window.py
Main application window — orchestrates all UI components.
"""

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter, QMessageBox, QFrame,
    QAbstractItemView, QSizePolicy, QApplication,
)
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QFont, QColor

from database.models import Post, ApiResponse
from logic.workers import (
    FetchPostsWorker, FetchPostDetailWorker,
    CreatePostWorker, UpdatePostWorker, DeletePostWorker,
)
from ui.detail_panel import DetailPanel
from ui.post_form_dialog import PostFormDialog
from style.theme import STYLESHEET


class MainWindow(QMainWindow):
    """Main application window for Post Manager."""

    def __init__(self):
        super().__init__()
        self.posts: list[Post] = []
        self.selected_post: Post | None = None
        self._active_workers = []  # keep references so GC doesn't kill threads

        self.setWindowTitle("Post Manager — pahrul.my.id")
        self.setMinimumSize(1100, 680)
        self.resize(1280, 760)
        self.setStyleSheet(STYLESHEET)

        self._build_ui()
        self._connect_signals()

        # Load posts on startup
        QTimer.singleShot(200, self.refresh_posts)

    # ─────────────────────────────────────────────────────────
    #   UI CONSTRUCTION
    # ─────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())
        root.addWidget(self._build_toolbar())
        root.addWidget(self._build_body(), 1)
        root.addWidget(self._build_status_bar())

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("header_widget")
        header.setFixedHeight(68)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(12)

        icon = QLabel("◈")
        icon.setStyleSheet("color: #F59E0B; font-size: 28px;")

        text_col = QWidget()
        text_layout = QVBoxLayout(text_col)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(1)

        title = QLabel("POST MANAGER")
        title.setObjectName("app_title")

        subtitle = QLabel("api.pahrul.my.id/api/posts  ·  CRUD Interface")
        subtitle.setObjectName("app_subtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        layout.addWidget(icon)
        layout.addWidget(text_col)
        layout.addStretch()

        # Post count badge
        self.post_count_label = QLabel("— posts")
        self.post_count_label.setStyleSheet(
            "color: #4B5563; font-size: 12px; font-weight: 600; letter-spacing: 1px;"
        )
        layout.addWidget(self.post_count_label)

        return header

    def _build_toolbar(self) -> QWidget:
        toolbar = QWidget()
        toolbar.setObjectName("toolbar_widget")
        toolbar.setFixedHeight(56)
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)

        self.btn_refresh = QPushButton("⟳  Refresh")
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.setFixedHeight(36)
        self.btn_refresh.setToolTip("Muat ulang daftar post (GET /api/posts)")

        self.btn_add = QPushButton("＋  Tambah Post")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setFixedHeight(36)
        self.btn_add.setToolTip("Tambah post baru (POST /api/posts)")

        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #2A2A2A;")
        sep.setFixedHeight(28)

        self.btn_edit = QPushButton("✎  Edit")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.setFixedHeight(36)
        self.btn_edit.setEnabled(False)
        self.btn_edit.setToolTip("Edit post terpilih (PUT /api/posts/{id})")

        self.btn_delete = QPushButton("✕  Hapus")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setFixedHeight(36)
        self.btn_delete.setEnabled(False)
        self.btn_delete.setToolTip("Hapus post terpilih (DELETE /api/posts/{id})")

        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_add)
        layout.addWidget(sep)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)
        layout.addStretch()

        # Loading indicator
        self.loading_label = QLabel("⏳  Memuat...")
        self.loading_label.setStyleSheet("color: #F59E0B; font-size: 12px; font-weight: 600;")
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

        return toolbar

    def _build_body(self) -> QWidget:
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(3)

        # ── Left: Table ──
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(16, 12, 8, 12)
        left_layout.setSpacing(8)

        table_header_row = QWidget()
        thr_layout = QHBoxLayout(table_header_row)
        thr_layout.setContentsMargins(0, 0, 0, 0)
        thr_layout.setSpacing(0)

        tbl_title = QLabel("DAFTAR POST")
        tbl_title.setStyleSheet(
            "color: #6B7280; font-size: 11px; font-weight: 700; letter-spacing: 2px;"
        )
        thr_layout.addWidget(tbl_title)
        thr_layout.addStretch()
        left_layout.addWidget(table_header_row)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "JUDUL", "PENULIS", "STATUS"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(3, 110)
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setDefaultSectionSize(46)
        self.table.setWordWrap(False)

        left_layout.addWidget(self.table)

        # ── Right: Detail panel ──
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(8, 12, 16, 12)
        right_layout.setSpacing(0)

        self.detail_panel = DetailPanel()
        right_layout.addWidget(self.detail_panel)

        splitter.addWidget(left_container)
        splitter.addWidget(right_container)
        splitter.setSizes([700, 400])

        wrapper = QWidget()
        wl = QVBoxLayout(wrapper)
        wl.setContentsMargins(0, 0, 0, 0)
        wl.addWidget(splitter)
        return wrapper

    def _build_status_bar(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("status_bar")
        bar.setFixedHeight(32)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)

        self.status_label = QLabel("Siap")
        self.status_label.setObjectName("status_label")
        self.status_label.setStyleSheet("color: #4B5563; font-size: 11px;")

        layout.addWidget(self.status_label)
        layout.addStretch()

        endpoint_label = QLabel("https://api.pahrul.my.id/api/posts")
        endpoint_label.setStyleSheet("color: #374151; font-size: 10px; font-family: monospace;")
        layout.addWidget(endpoint_label)

        return bar

    # ─────────────────────────────────────────────────────────
    #   SIGNAL CONNECTIONS
    # ─────────────────────────────────────────────────────────

    def _connect_signals(self):
        self.btn_refresh.clicked.connect(self.refresh_posts)
        self.btn_add.clicked.connect(self.open_add_dialog)
        self.btn_edit.clicked.connect(self.open_edit_dialog)
        self.btn_delete.clicked.connect(self.confirm_delete)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(lambda: self.open_edit_dialog())

    # ─────────────────────────────────────────────────────────
    #   TABLE HELPERS
    # ─────────────────────────────────────────────────────────

    def _populate_table(self, posts: list[Post]):
        self.table.setRowCount(0)
        self.posts = posts

        for row, post in enumerate(posts):
            self.table.insertRow(row)

            id_item = QTableWidgetItem(str(post.id))
            id_item.setTextAlignment(Qt.AlignCenter)
            id_item.setForeground(QColor("#6B7280"))

            title_item = QTableWidgetItem(post.title)
            title_item.setForeground(QColor("#E8E8E8"))

            author_item = QTableWidgetItem(post.author)
            author_item.setForeground(QColor("#9CA3AF"))

            status_item = QTableWidgetItem(post.status.upper())
            status_item.setTextAlignment(Qt.AlignCenter)
            if post.status == "published":
                status_item.setForeground(QColor("#4ADE80"))
                status_item.setBackground(QColor("#0A2A14"))
            else:
                status_item.setForeground(QColor("#A8A29E"))
                status_item.setBackground(QColor("#1C1917"))

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, title_item)
            self.table.setItem(row, 2, author_item)
            self.table.setItem(row, 3, status_item)

        count = len(posts)
        self.post_count_label.setText(f"{count} post{'s' if count != 1 else ''}")

    def _get_selected_post(self) -> Post | None:
        rows = self.table.selectedItems()
        if not rows:
            return None
        row = self.table.currentRow()
        if row < 0 or row >= len(self.posts):
            return None
        return self.posts[row]

    # ─────────────────────────────────────────────────────────
    #   STATE HELPERS
    # ─────────────────────────────────────────────────────────

    def _set_loading(self, loading: bool, message: str = "Memuat..."):
        self.loading_label.setText(f"⏳  {message}")
        self.loading_label.setVisible(loading)
        self.btn_refresh.setEnabled(not loading)
        self.btn_add.setEnabled(not loading)
        if loading:
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)

    def _set_status(self, message: str, kind: str = "info"):
        colors = {"info": "#4B5563", "success": "#4ADE80", "error": "#F87171", "loading": "#F59E0B"}
        color = colors.get(kind, "#4B5563")
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 11px;")

    def _show_error_dialog(self, title: str, message: str, extra: dict = None):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Warning)
        full_msg = message
        if extra:
            details = "\n".join(f"  • {k}: {v}" for k, v in extra.items())
            full_msg += f"\n\nDetail validasi:\n{details}"
        msg.setText(full_msg)
        msg.setStyleSheet("""
            QMessageBox { background-color: #1A1A1A; color: #E8E8E8; }
            QPushButton { background-color: #252525; color: #D1D5DB; border: 1px solid #333; border-radius: 6px; padding: 6px 18px; }
            QPushButton:hover { border-color: #F59E0B; color: #F59E0B; }
        """)
        msg.exec()

    def _show_success_dialog(self, title: str, message: str):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox { background-color: #1A1A1A; color: #E8E8E8; }
            QPushButton { background-color: #252525; color: #D1D5DB; border: 1px solid #333; border-radius: 6px; padding: 6px 18px; }
            QPushButton:hover { border-color: #4ADE80; color: #4ADE80; }
        """)
        msg.exec()

    # ─────────────────────────────────────────────────────────
    #   SLOTS: SELECTION
    # ─────────────────────────────────────────────────────────

    @Slot()
    def on_selection_changed(self):
        post = self._get_selected_post()
        has_selection = post is not None
        self.btn_edit.setEnabled(has_selection)
        self.btn_delete.setEnabled(has_selection)

        if post:
            self.selected_post = post
            self.load_post_detail(post.id)

    # ─────────────────────────────────────────────────────────
    #   SLOTS: REFRESH / GET ALL
    # ─────────────────────────────────────────────────────────

    @Slot()
    def refresh_posts(self):
        self._set_loading(True, "Memuat daftar post...")
        self._set_status("Menghubungi server...", "loading")
        self.detail_panel.reset()
        self.table.clearSelection()
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.selected_post = None

        worker = FetchPostsWorker()
        worker.finished.connect(self._on_posts_fetched)
        self._active_workers.append(worker)
        worker.start()

    @Slot(object)
    def _on_posts_fetched(self, result: ApiResponse):
        self._set_loading(False)
        worker = self.sender()
        if worker in self._active_workers:
            self._active_workers.remove(worker)

        if result.success:
            self._populate_table(result.data)
            self._set_status(f"Berhasil memuat {len(result.data)} post.", "success")
        else:
            self._set_status(f"Gagal memuat post: {result.error_message}", "error")
            self._show_error_dialog("Gagal Memuat Data", result.error_message)

    # ─────────────────────────────────────────────────────────
    #   SLOTS: DETAIL
    # ─────────────────────────────────────────────────────────

    def load_post_detail(self, post_id: int):
        self.detail_panel.show_loading()

        worker = FetchPostDetailWorker(post_id)
        worker.finished.connect(self._on_detail_fetched)
        self._active_workers.append(worker)
        worker.start()

    @Slot(object)
    def _on_detail_fetched(self, result: ApiResponse):
        worker = self.sender()
        if worker in self._active_workers:
            self._active_workers.remove(worker)

        if result.success:
            self.detail_panel.show_post(result.data)
        else:
            self.detail_panel.show_error(result.error_message)

    # ─────────────────────────────────────────────────────────
    #   SLOTS: ADD
    # ─────────────────────────────────────────────────────────

    @Slot()
    def open_add_dialog(self):
        dialog = PostFormDialog(self)
        dialog.submitted.connect(self._on_add_submitted)
        dialog.exec()

    @Slot(dict)
    def _on_add_submitted(self, payload: dict):
        dialog: PostFormDialog = self.sender().parent() if hasattr(self.sender(), 'parent') else None
        # Find active dialog
        dialog = None
        for w in self.children():
            if isinstance(w, PostFormDialog):
                dialog = w
                break

        if dialog:
            dialog.set_loading(True)

        self._set_status("Menambah post baru...", "loading")

        worker = CreatePostWorker(payload)
        worker.finished.connect(lambda r: self._on_add_done(r, dialog))
        self._active_workers.append(worker)
        worker.start()

    def _on_add_done(self, result: ApiResponse, dialog: PostFormDialog):
        worker = self.sender()
        if worker in self._active_workers:
            self._active_workers.remove(worker)

        if dialog:
            dialog.set_loading(False)

        if result.success:
            post: Post = result.data
            if dialog:
                dialog.accept()
            self._set_status(f"Post berhasil ditambahkan! ID: {post.id}", "success")
            self._show_success_dialog(
                "Post Ditambahkan",
                f"✓ Post berhasil dibuat!\n\nID: {post.id}\nJudul: {post.title}"
            )
            self.refresh_posts()
        else:
            if dialog:
                if result.status_code == 422:
                    err_text = result.error_message
                    if result.validation_errors:
                        details = " | ".join(f"{k}: {v}" for k, v in result.validation_errors.items())
                        err_text += f"\n{details}"
                    dialog.show_error(err_text)
                else:
                    dialog.show_error(result.error_message)
            self._set_status(f"Gagal menambah post: {result.error_message}", "error")

    # ─────────────────────────────────────────────────────────
    #   SLOTS: EDIT
    # ─────────────────────────────────────────────────────────

    @Slot()
    def open_edit_dialog(self):
        post = self._get_selected_post()
        if not post:
            return

        dialog = PostFormDialog(self, post=post)
        dialog.submitted.connect(lambda payload: self._on_edit_submitted(payload, post.id, dialog))
        dialog.exec()

    def _on_edit_submitted(self, payload: dict, post_id: int, dialog: PostFormDialog):
        dialog.set_loading(True)
        self._set_status("Menyimpan perubahan...", "loading")

        worker = UpdatePostWorker(post_id, payload)
        worker.finished.connect(lambda r: self._on_edit_done(r, dialog))
        self._active_workers.append(worker)
        worker.start()

    def _on_edit_done(self, result: ApiResponse, dialog: PostFormDialog):
        worker = self.sender()
        if worker in self._active_workers:
            self._active_workers.remove(worker)

        dialog.set_loading(False)

        if result.success:
            post: Post = result.data
            dialog.accept()
            self._set_status(f"Post berhasil diperbarui! ID: {post.id}", "success")
            self._show_success_dialog(
                "Post Diperbarui",
                f"✓ Post berhasil diperbarui!\n\nID: {post.id}\nJudul: {post.title}"
            )
            self.refresh_posts()
        else:
            if result.status_code == 422:
                err_text = result.error_message
                if result.validation_errors:
                    details = " | ".join(f"{k}: {v}" for k, v in result.validation_errors.items())
                    err_text += f"\n{details}"
                dialog.show_error(err_text)
            else:
                dialog.show_error(result.error_message)
            self._set_status(f"Gagal memperbarui post: {result.error_message}", "error")

    # ─────────────────────────────────────────────────────────
    #   SLOTS: DELETE
    # ─────────────────────────────────────────────────────────

    @Slot()
    def confirm_delete(self):
        post = self._get_selected_post()
        if not post:
            return

        confirm = QMessageBox(self)
        confirm.setWindowTitle("Konfirmasi Hapus")
        confirm.setIcon(QMessageBox.Warning)
        confirm.setText(
            f"Hapus post ini?\n\n"
            f"ID: {post.id}\n"
            f"Judul: {post.title}\n\n"
            f"⚠ Semua komentar akan ikut terhapus (cascade delete)."
        )
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        confirm.button(QMessageBox.Yes).setText("Ya, Hapus")
        confirm.button(QMessageBox.No).setText("Batal")
        confirm.setStyleSheet("""
            QMessageBox { background-color: #1A1A1A; color: #E8E8E8; }
            QPushButton { background-color: #252525; color: #D1D5DB; border: 1px solid #333; border-radius: 6px; padding: 6px 18px; min-width: 80px; }
            QPushButton:hover { border-color: #EF4444; color: #FCA5A5; }
        """)

        if confirm.exec() != QMessageBox.Yes:
            return

        self._do_delete(post)

    def _do_delete(self, post: Post):
        self._set_loading(True, f"Menghapus post ID {post.id}...")
        self._set_status(f"Menghapus post '{post.title}'...", "loading")

        worker = DeletePostWorker(post.id)
        worker.finished.connect(lambda r: self._on_delete_done(r, post))
        self._active_workers.append(worker)
        worker.start()

    def _on_delete_done(self, result: ApiResponse, post: Post):
        worker = self.sender()
        if worker in self._active_workers:
            self._active_workers.remove(worker)

        self._set_loading(False)

        if result.success:
            self._set_status(f"Post '{post.title}' berhasil dihapus.", "success")
            self.detail_panel.reset()
            self.selected_post = None
            self.refresh_posts()
        else:
            self._set_status(f"Gagal menghapus: {result.error_message}", "error")
            self._show_error_dialog("Gagal Menghapus", result.error_message)
