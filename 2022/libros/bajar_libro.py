# https://github.com/c-w/gutenberg/
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers


text = strip_headers(load_etext(2701)).strip()
text = load_etext(2701)
text = text.replace('\n', ' ')
print(len(text))
with open('moby_dick.txt', 'w', encoding="utf-8") as f:
    f.write(text)
