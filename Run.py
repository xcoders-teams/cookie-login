import requests
from bs4 import BeautifulSoup
import random


def change_url(option):
    url_dict = {
        '1': {'url': 'https://www.facebook.com/login', 'name': 'Facebook'},
        '2': {'url': 'https://www.instagram.com/accounts/login', 'name': 'Instagram'},
        '3': {'url': 'https://twitter.com/login', 'name': 'Twitter'},
        '4': {'url': 'https://accounts.google.com/signin/v2/identifier', 'name': 'Gmail'},
        '5': {'url': 'https://www.youtube.com', 'name': 'Youtube'},
        '6': {'url': 'https://discord.com/login', 'name': 'Discord'},
        '7': {'url': 'https://web.telegram.org/k', 'name': 'Telegram'}
    }
    try:
        url = url_dict[option]['url']
        print(f"Sedang menyiapkan web {url_dict[option]['name']}...")
        return url
    except KeyError:
        print("Maaf, pilihan tidak tersedia")
        exit()


def generate_random_color():
    color = '#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color


def print_colored_text(text):
    color = generate_random_color()
    print(f"\033[38;2;{color}m{text}\033[38;2;255m")


def main():
    print("Selamat datang di skrip login otomatis!\n")
    url_option = input("Silakan pilih URL yang akan diakses:\n1. Facebook\n2. Instagram\n3. Twitter\n4. Gmail\n5. Youtube\n6. Discord\n7. Telegram\n\n")
    url = change_url(url_option)

    session = requests.Session()
    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': 'authenticity_token'})
    if token_input is not None:
        token = token_input.get('value')
    else:
        print_colored_text("Tidak dapat menemukan authenticity_token")
        exit()

    username = input("Masukkan username atau email: ")
    password = input("Masukkan password: ")

    if not username or not password:
        print_colored_text("Username atau password tidak boleh kosong")
        exit()

    data = {
        'session[username_or_email]': username,
        'session[password]': password,
        'authenticity_token': token
    }

    response = session.post(url, data=data)

    cookies = session.cookies.get_dict()

    if 'twofactor' in response.url:
        print_colored_text('Login berhasil! Harap matikan autentikasi dua faktor untuk menggunakan skrip ini')
        with open(f'result/{url_option}_success_cookies.txt', 'w') as f:
            for key, value in cookies.items():
                f.write('%s:%s\n' % (key, value))
    else:
        print_colored_text(f'Gagal login ke {url_option}')
        with open(f'result/{url_option}_failed_cookies.txt', 'w') as f:
            for key, value in cookies.items():
                f.write('%s:%s\n' % (key, value))


if __name__ == '__main__':
    main()