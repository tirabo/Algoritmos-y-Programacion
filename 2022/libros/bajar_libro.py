# https://github.com/c-w/gutenberg/
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers


text = strip_headers(load_etext(2701)).strip()
text = load_etext(2701)
text = text.replace('\r\n', '\n')
text = text.replace('\n\n', '\n')
print(len(text))
with open('moby_dick.txt', 'w', encoding="utf-8") as f:
    f.write(text)

text = strip_headers(load_etext(44112)).strip()
text = load_etext(44112)
text = text.replace('\r\n', '\n')
text = text.replace('\n\n', '\n')
print(len(text))
with open('ARGENTINA_LEGEND_AND_HISTORY.txt', 'w', encoding="utf-8") as f:
    f.write(text)