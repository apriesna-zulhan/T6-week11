"""
style/theme.py
Application stylesheet — dark industrial theme with amber accents.
"""

STYLESHEET = """
/* ─────────────────────────────────────────
   Global
───────────────────────────────────────── */
* {
    font-family: 'Segoe UI', 'Ubuntu', 'Helvetica Neue', sans-serif;
    font-size: 13px;
    color: #E8E8E8;
}

QMainWindow, QDialog {
    background-color: #141414;
}

QWidget {
    background-color: #141414;
}

/* ─────────────────────────────────────────
   Header / Title Bar
───────────────────────────────────────── */
#header_widget {
    background-color: #1A1A1A;
    border-bottom: 2px solid #F59E0B;
}

#app_title {
    font-size: 22px;
    font-weight: 700;
    color: #F59E0B;
    letter-spacing: 2px;
}

#app_subtitle {
    font-size: 11px;
    color: #6B7280;
    letter-spacing: 1px;
}

/* ─────────────────────────────────────────
   Toolbar / Action Buttons
───────────────────────────────────────── */
#toolbar_widget {
    background-color: #1C1C1C;
    border-bottom: 1px solid #2A2A2A;
    padding: 6px 0px;
}

QPushButton {
    background-color: #252525;
    color: #D1D5DB;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

QPushButton:hover {
    background-color: #2E2E2E;
    border-color: #F59E0B;
    color: #F59E0B;
}

QPushButton:pressed {
    background-color: #1A1A1A;
}

QPushButton:disabled {
    background-color: #1E1E1E;
    color: #3D3D3D;
    border-color: #252525;
}

QPushButton#btn_add {
    background-color: #252525; /* Sama dengan tombol batal */
    color: #FFFFFF;            /* Teks putih sesuai request */
    border: 1px solid #333333; /* Border halus */
    font-weight: 700;          /* Tetap tebal agar beda dikit dari batal */
}

QPushButton#btn_add:hover {
    background-color: #2E2E2E; 
    border-color: #FFFFFF;     /* Saat hover, border jadi putih */
    color: #FFFFFF;
}

QPushButton#btn_add:pressed {
    background-color: #1A1A1A;
}

QPushButton#btn_refresh {
    background-color: #1F2937;
    color: #9CA3AF;
    border-color: #374151;
}

QPushButton#btn_refresh:hover {
    border-color: #F59E0B;
    color: #F59E0B;
}

QPushButton#btn_edit {
    border-color: #3B82F6;
    color: #93C5FD;
}

QPushButton#btn_edit:hover {
    background-color: #1D3461;
    border-color: #60A5FA;
    color: #BFDBFE;
}

QPushButton#btn_delete {
    border-color: #EF4444;
    color: #FCA5A5;
}

QPushButton#btn_delete:hover {
    background-color: #450A0A;
    border-color: #F87171;
    color: #FECACA;
}

/* ─────────────────────────────────────────
   Table
───────────────────────────────────────── */
QTableWidget {
    background-color: #181818;
    border: 1px solid #262626;
    border-radius: 8px;
    gridline-color: #222222;
    selection-background-color: #2A2000;
    selection-color: #F59E0B;
    alternate-background-color: #1C1C1C;
}

QTableWidget::item {
    padding: 10px 12px;
    border-bottom: 1px solid #222222;
}

QTableWidget::item:selected {
    background-color: #2A2000;
    color: #F59E0B;
    border-left: 3px solid #F59E0B;
}

QTableWidget::item:hover {
    background-color: #1F1F1F;
}

QHeaderView::section {
    background-color: #1A1A1A;
    color: #9CA3AF;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid #F59E0B;
    border-right: 1px solid #262626;
}

QHeaderView::section:last {
    border-right: none;
}

/* ─────────────────────────────────────────
   Detail Panel
───────────────────────────────────────── */
#detail_panel {
    background-color: #181818;
    border: 1px solid #262626;
    border-radius: 8px;
}

#detail_title {
    font-size: 15px;
    font-weight: 700;
    color: #F59E0B;
    letter-spacing: 0.5px;
}

#detail_section_label {
    font-size: 10px;
    font-weight: 700;
    color: #6B7280;
    letter-spacing: 2px;
    text-transform: uppercase;
}

#detail_value {
    color: #D1D5DB;
    font-size: 13px;
}

#status_badge_published {
    background-color: #052E16;
    color: #4ADE80;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

#status_badge_draft {
    background-color: #1C1917;
    color: #A8A29E;
    border: 1px solid #44403C;
    border-radius: 10px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

/* ─────────────────────────────────────────
   Form / Dialog
───────────────────────────────────────── */
QDialog {
    background-color: #1A1A1A;
    border: 1px solid #333333;
}

QLabel {
    color: #9CA3AF;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

QLineEdit, QTextEdit, QComboBox {
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 8px 12px;
    color: #E8E8E8;
    font-size: 13px;
    selection-background-color: #F59E0B;
    selection-color: #141414;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #F59E0B;
    background-color: #130E00;
}

QLineEdit:hover, QTextEdit:hover {
    border-color: #444444;
}

QComboBox {
    padding-right: 24px;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #9CA3AF;
    width: 0;
    height: 0;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #1C1C1C;
    border: 1px solid #333333;
    selection-background-color: #F59E0B;
    selection-color: #141414;
    outline: none;
}

QTextEdit {
    line-height: 1.5;
}

/* ─────────────────────────────────────────
   Status Bar
───────────────────────────────────────── */
#status_bar {
    background-color: #111111;
    border-top: 1px solid #1F1F1F;
    padding: 4px 16px;
}

#status_label {
    color: #6B7280;
    font-size: 11px;
}

#status_label[status="success"] {
    color: #4ADE80;
}

#status_label[status="error"] {
    color: #F87171;
}

#status_label[status="loading"] {
    color: #F59E0B;
}

/* ─────────────────────────────────────────
   Loading Overlay
───────────────────────────────────────── */
#loading_overlay {
    background-color: rgba(20, 20, 20, 200);
    border-radius: 8px;
}

#loading_label {
    color: #F59E0B;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* ─────────────────────────────────────────
   Scrollbar
───────────────────────────────────────── */
QScrollBar:vertical {
    background-color: #141414;
    width: 8px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #333333;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #F59E0B;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #141414;
    height: 8px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #333333;
    border-radius: 4px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #F59E0B;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* ─────────────────────────────────────────
   Separator
───────────────────────────────────────── */
QFrame[frameShape="4"], QFrame[frameShape="5"] {
    color: #262626;
}

/* ─────────────────────────────────────────
   Message / Error box
───────────────────────────────────────── */
#error_box {
    background-color: #1C0000;
    border: 1px solid #7F1D1D;
    border-radius: 6px;
    padding: 10px 14px;
}

#error_box QLabel {
    color: #FCA5A5;
    font-size: 12px;
}

#info_box {
    background-color: #052E16;
    border: 1px solid #166534;
    border-radius: 6px;
    padding: 10px 14px;
}

#info_box QLabel {
    color: #4ADE80;
    font-size: 12px;
}

/* ─────────────────────────────────────────
   Comments section
───────────────────────────────────────── */
#comment_card {
    background-color: #1C1C1C;
    border: 1px solid #262626;
    border-left: 3px solid #F59E0B;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 6px;
}

#comment_author {
    font-weight: 700;
    color: #F59E0B;
    font-size: 12px;
}

#comment_body {
    color: #9CA3AF;
    font-size: 12px;
    margin-top: 4px;
}

/* ─────────────────────────────────────────
   Splitter
───────────────────────────────────────── */
QSplitter::handle {
    background-color: #262626;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #F59E0B;
}
"""

COLORS = {
    "accent": "#F59E0B",
    "bg_primary": "#141414",
    "bg_secondary": "#1A1A1A",
    "bg_card": "#181818",
    "text_primary": "#E8E8E8",
    "text_secondary": "#9CA3AF",
    "border": "#262626",
    "success": "#4ADE80",
    "error": "#F87171",
    "info": "#60A5FA",
}
