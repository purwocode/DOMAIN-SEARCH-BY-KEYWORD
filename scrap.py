import requests
from bs4 import BeautifulSoup
import re

def scrape_emails(url):
    try:
        # Kirim permintaan HTTP ke URL
        response = requests.get(url)
        
        # Periksa jika permintaan berhasil
        if response.status_code == 200:
            # Parsing konten HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cari semua teks yang tampak seperti alamat email dalam teks
            email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
            emails = set(email_pattern.findall(soup.get_text()))
            
            # Cari email dalam atribut href di tag <a>
            mailto_links = soup.find_all('a', href=True)
            for link in mailto_links:
                href = link['href']
                if href.startswith('mailto:'):
                    email = href[len('mailto:'):]
                    if email_pattern.match(email):
                        emails.add(email)
            
            return emails
        else:
            print(f"Gagal mengakses halaman {url}. Status Code: {response.status_code}")
            return set()
    except requests.RequestException as e:
        print(f"Terjadi kesalahan: {e}")
        return set()

def main():
    # Baca URL dari file link.txt
    try:
        with open('link.txt', 'r') as file:
            urls = file.readlines()
            
        with open('email.txt', 'a') as email_file:  # Buka file email.txt dalam mode append
            for url in urls:
                url = url.strip()
                if url:  # Pastikan URL tidak kosong
                    print(f"Memproses URL: {url}")
                    emails = scrape_emails(url)
                    
                    # Simpan hasil email ke file dan tampilkan di konsol
                    if emails:
                        email_file.write(f"URL: {url}\n")
                        for email in emails:
                            email_file.write(f"{email}\n")
                            print(f"Email ditemukan: {email}")
                        email_file.write("\n")
                        print(f"Ditemukan email di {url} dan disimpan ke email.txt")
                    else:
                        print(f"Tidak ada email ditemukan di {url}")
    
    except FileNotFoundError:
        print("File 'link.txt' tidak ditemukan.")

if __name__ == "__main__":
    main()
