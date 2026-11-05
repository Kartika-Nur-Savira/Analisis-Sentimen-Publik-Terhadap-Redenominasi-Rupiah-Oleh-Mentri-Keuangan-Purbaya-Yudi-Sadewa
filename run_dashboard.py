"""
run_dashboard.py
Menjalankan server web lokal ringan untuk membuka dashboard analisis sentimen
secara otomatis di browser Anda.
"""

import os
import sys
import webbrowser
import http.server
import socketserver

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        # Meredam logging berlebih
        pass

def main():
    os.chdir(DIRECTORY)
    server_address = ("", PORT)

    # Cek apakah port tersedia atau fallback ke port lain
    actual_port = PORT
    httpd = None
    for p in range(PORT, PORT + 10):
        try:
            httpd = socketserver.TCPServer(("", p), Handler)
            actual_port = p
            break
        except OSError:
            continue

    if not httpd:
        print(f"❌ Tidak dapat membuka port di range {PORT}-{PORT+10}")
        sys.exit(1)

    url = f"http://localhost:{actual_port}/index.html"
    print("=" * 65)
    print("📊 DASHBOARD ANALISIS SENTIMEN REDENOMINASI RUPIAH")
    print("=" * 65)
    print(f"🚀 Server aktif di: {url}")
    print("💡 Membuka browser web default secara otomatis...")
    print("Tekan Ctrl+C untuk menghentikan server.")
    print("=" * 65)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server dihentikan.")
        httpd.server_close()

if __name__ == "__main__":
    main()

