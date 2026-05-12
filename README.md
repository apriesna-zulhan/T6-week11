# Post Manager — PySide6 Desktop App

Aplikasi desktop untuk mengelola data post menggunakan API `https://api.pahrul.my.id/api/posts`.

## Fitur
- ✅ Tampilkan daftar post (GET /api/posts)
- ✅ Detail post + komentar (GET /api/posts/{id})
- ✅ Tambah post baru (POST /api/posts)
- ✅ Edit post (PUT /api/posts/{id})
- ✅ Hapus post dengan konfirmasi dialog (DELETE /api/posts/{id}) — cascade delete comments
- ✅ Threading: semua API call di QThread terpisah, UI tidak freeze
- ✅ Loading state & error handling (timeout, connection error, 422 validation)
- ✅ Auto-generate slug dari judul
- ✅ Validasi 422 ditampilkan ke user

## Struktur Folder
```
post_manager/
├── main.py                  # Entry point
├── requirements.txt         # Dependensi
├── database/
│   ├── __init__.py
│   └── models.py            # Data models: Post, Comment, ApiResponse
├── logic/
│   ├── __init__.py
│   ├── api_client.py        # HTTP client (requests)
│   └── workers.py           # QThread workers
├── style/
│   ├── __init__.py
│   └── theme.py             # QSS stylesheet & color palette
└── ui/
    ├── __init__.py
    ├── main_window.py       # Main window
    ├── detail_panel.py      # Right-side detail panel
    └── post_form_dialog.py  # Add/Edit dialog
```

## Cara Menjalankan

### 1. Install dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi
```bash
python main.py
```

## Dependensi
- Python 3.10+
- PySide6 >= 6.6.0
- requests >= 2.31.0

## Endpoint API
| Operasi          | Method | Endpoint             |
|------------------|--------|----------------------|
| Tampilkan semua  | GET    | /api/posts           |
| Detail satu post | GET    | /api/posts/{id}      |
| Tambah post      | POST   | /api/posts           |
| Edit post        | PUT    | /api/posts/{id}      |
| Hapus post       | DELETE | /api/posts/{id}      |
