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

## Screenshoots
### 1. Tampilan awal
<img width="1409" height="1141" alt="image" src="https://github.com/user-attachments/assets/15cfda23-718b-4c87-82be-5b04200b93b2" />

### 2. Menambahkan Postingan
<img width="1418" height="1149" alt="image" src="https://github.com/user-attachments/assets/15e0f971-3bab-4e77-aaf8-681ac2929b35" />

### 3. Mengedit Postingan
<img width="1420" height="1145" alt="image" src="https://github.com/user-attachments/assets/2ec4c5bb-532b-4321-bb54-64250a4dea29" />

### 4. Melihat Detail Postingan
<img width="493" height="554" alt="image" src="https://github.com/user-attachments/assets/ff7ef2f5-4b0d-48f5-bb16-e9ad1f1a00b9" />

### 5. Menghapus Postingan
<img width="1415" height="1146" alt="image" src="https://github.com/user-attachments/assets/ad9ea0f2-e2df-4d5a-b183-e4592c5b9843" />

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
