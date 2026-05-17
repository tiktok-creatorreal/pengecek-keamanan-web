import urllib.request
import urllib.parse
import sys

# === KONFIGURASI TELEGRAM & TARGET ===
TELEGRAM_TOKEN = "8762651077:AAHAbyLHR3DRVNEWxSXbO7kDi2PS-vV9A1A"
CHAT_ID = "1966317946"
TARGET_URL = "https://tiktok-creatorreal.github.io/Dewianisa/?sender=1966317946`"
# =====================================

def kirim_notifikasi_telegram(pesan):
    """Mengirim pesan peringatan langsung ke bot Telegram Anda"""
    try:
        url_encoded_msg = urllib.parse.quote(pesan)
        api_url = f"https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={url_encoded_msg}&parse_mode=Markdown"
        
        # Eksekusi permintaan HTTP ke API Telegram
        urllib.request.urlopen(api_url, timeout=10)
        print("[+] Notifikasi bahaya berhasil dikirim ke Telegram!")
    except Exception as e:
        print(f"[-] Gagal mengirim pesan ke Telegram: {e}")

def cek_keamanan_website(url):
    """Memeriksa celah keamanan clickjacking pada HTTP Headers"""
    print(f"[*] Memulai pemindaian pada: {url}")
    
    # Memastikan format URL benar
    if not url.startswith("http"):
        url = "https://" + url

    try:
        # Membuka koneksi ke website target
        response = urllib.request.urlopen(url, timeout=10)
        headers = response.info()
        
        # Ubah semua nama header ke huruf kecil untuk akurasi pencarian
        headers_lower = [h.lower() for h in headers.keys()]
        
        masalah = []
        
        # 1. Periksa X-Frame-Options
        if "x-frame-options" not in headers_lower:
            masalah.append("- Header `X-Frame-Options` tidak ditemukan.")
            
        # 2. Periksa Content-Security-Policy (CSP) untuk frame-ancestors
        if "content-security-policy" in headers_lower:
            csp_value = headers.get("Content-Security-Policy", "").lower()
            if "frame-ancestors" not in csp_value:
                masalah.append("- Header `CSP` ada, tetapi aturan `frame-ancestors` tidak dikonfigurasi.")
        else:
            masalah.append("- Header `Content-Security-Policy` (CSP) tidak ditemukan.")

        # Evaluasi Hasil Pemeriksaan
        if masalah:
            print("[-] Website RENTAN terhadap Clickjacking!")
            
            # Format pesan teks untuk dikirim ke Telegram
            rincian_masalah = "\n".join(masalah)
            pesan_alert = (
                f"🚨 *PERINGATAN KEAMANAN WEBSITE* 🚨\n\n"
                f"⚠️ Website Anda *RENTAN* terhadap serangan Clickjacking!\n\n"
                f"🌐 *Target:* {url}\n"
                f"🔍 *Temuan Masalah:*\n{rincian_masalah}\n\n"
                f"💡 *Solusi:* Segera tambahkan header `X-Frame-Options: SAMEORIGIN` pada konfigurasi server Anda."
            )
            
            kirim_notifikasi_telegram(pesan_alert)
        else:
            print("[+] Website AMAN! Semua header proteksi clickjacking aktif.")
            
    except Exception as e:
        print(f"[-] Gagal memuat website atau koneksi terputus: {e}")

if __name__ == "__main__":
    cek_keamanan_website(TARGET_URL)
