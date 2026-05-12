"""
logic/api_client.py
HTTP API client for Post Manager — handles all requests to the backend.
"""

import requests
from typing import Optional, List
from database.models import Post, ApiResponse

BASE_URL = "https://api.pahrul.my.id/api"
TIMEOUT = 15  # seconds


class PostApiClient:
    """Client for interacting with the Posts API."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _handle_response(self, response: requests.Response) -> ApiResponse:
        """Parse and wrap an HTTP response into ApiResponse."""
        try:
            json_data = response.json()
        except Exception:
            json_data = {}

        if response.status_code == 422:
            # Validation error — extract field messages
            errors = {}
            if isinstance(json_data, dict):
                errors = json_data.get("errors", json_data.get("message", {}))
            return ApiResponse(
                success=False,
                error_message="Validasi gagal — periksa kembali data yang dimasukkan.",
                status_code=422,
                validation_errors=errors if isinstance(errors, dict) else {"detail": str(errors)},
            )

        if not response.ok:
            msg = json_data.get("message", f"HTTP Error {response.status_code}") if isinstance(json_data, dict) else f"HTTP Error {response.status_code}"
            return ApiResponse(
                success=False,
                error_message=msg,
                status_code=response.status_code,
            )

        return ApiResponse(success=True, data=json_data, status_code=response.status_code)

    def get_all_posts(self) -> ApiResponse:
        """GET /api/posts — fetch all posts."""
        try:
            resp = self.session.get(f"{self.base_url}/posts", timeout=TIMEOUT)
            result = self._handle_response(resp)
            if result.success:
                raw = result.data
                # API may return list directly or wrapped in a key
                if isinstance(raw, list):
                    posts = [Post.from_dict(p) for p in raw]
                elif isinstance(raw, dict):
                    items = raw.get("data", raw.get("posts", []))
                    posts = [Post.from_dict(p) for p in items]
                else:
                    posts = []
                result.data = posts
            return result
        except requests.Timeout:
            return ApiResponse(success=False, error_message="Koneksi timeout — server tidak merespons.")
        except requests.ConnectionError:
            return ApiResponse(success=False, error_message="Gagal terhubung ke server — periksa koneksi internet Anda.")
        except Exception as e:
            return ApiResponse(success=False, error_message=f"Error tidak terduga: {str(e)}")

    def get_post(self, post_id: int) -> ApiResponse:
        """GET /api/posts/{id} — fetch single post with comments."""
        try:
            resp = self.session.get(f"{self.base_url}/posts/{post_id}", timeout=TIMEOUT)
            result = self._handle_response(resp)
            if result.success:
                raw = result.data
                if isinstance(raw, dict):
                    post_data = raw.get("data", raw)
                    result.data = Post.from_dict(post_data)
            return result
        except requests.Timeout:
            return ApiResponse(success=False, error_message="Koneksi timeout — server tidak merespons.")
        except requests.ConnectionError:
            return ApiResponse(success=False, error_message="Gagal terhubung ke server — periksa koneksi internet Anda.")
        except Exception as e:
            return ApiResponse(success=False, error_message=f"Error tidak terduga: {str(e)}")

    def create_post(self, payload: dict) -> ApiResponse:
        """POST /api/posts — create a new post."""
        try:
            resp = self.session.post(f"{self.base_url}/posts", json=payload, timeout=TIMEOUT)
            result = self._handle_response(resp)
            if result.success:
                raw = result.data
                if isinstance(raw, dict):
                    post_data = raw.get("data", raw)
                    result.data = Post.from_dict(post_data)
            return result
        except requests.Timeout:
            return ApiResponse(success=False, error_message="Koneksi timeout — server tidak merespons.")
        except requests.ConnectionError:
            return ApiResponse(success=False, error_message="Gagal terhubung ke server — periksa koneksi internet Anda.")
        except Exception as e:
            return ApiResponse(success=False, error_message=f"Error tidak terduga: {str(e)}")

    def update_post(self, post_id: int, payload: dict) -> ApiResponse:
        """PUT /api/posts/{id} — update an existing post."""
        try:
            resp = self.session.put(f"{self.base_url}/posts/{post_id}", json=payload, timeout=TIMEOUT)
            result = self._handle_response(resp)
            if result.success:
                raw = result.data
                if isinstance(raw, dict):
                    post_data = raw.get("data", raw)
                    result.data = Post.from_dict(post_data)
            return result
        except requests.Timeout:
            return ApiResponse(success=False, error_message="Koneksi timeout — server tidak merespons.")
        except requests.ConnectionError:
            return ApiResponse(success=False, error_message="Gagal terhubung ke server — periksa koneksi internet Anda.")
        except Exception as e:
            return ApiResponse(success=False, error_message=f"Error tidak terduga: {str(e)}")

    def delete_post(self, post_id: int) -> ApiResponse:
        """DELETE /api/posts/{id} — delete a post (cascade deletes comments)."""
        try:
            resp = self.session.delete(f"{self.base_url}/posts/{post_id}", timeout=TIMEOUT)
            result = self._handle_response(resp)
            return result
        except requests.Timeout:
            return ApiResponse(success=False, error_message="Koneksi timeout — server tidak merespons.")
        except requests.ConnectionError:
            return ApiResponse(success=False, error_message="Gagal terhubung ke server — periksa koneksi internet Anda.")
        except Exception as e:
            return ApiResponse(success=False, error_message=f"Error tidak terduga: {str(e)}")
