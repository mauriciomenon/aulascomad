import pyshorteners

def shorten_url(long_url):
    try:
        type_tiny = pyshorteners.Shortener(timeout=10)  # Aumente o tempo limite para 10 segundos
        short_url = type_tiny.tinyurl.short(long_url)
        return short_url
    except Exception as e:
        return f"Erro ao encurtar URL: {e}"

if __name__ == "__main__":
    long_url = input("Enter the URL to shorten: ")
    short_url = shorten_url(long_url)
    print("The Shortened URL is: " + short_url)
