import gutenbergpy.textget


#this gets a book by its gutenberg id
raw_book    = gutenbergpy.textget.get_text_by_id(1000)
# print(raw_book)
#this strips the headers from the book
clean_book  = gutenbergpy.textget.strip_headers(raw_book)
# print(clean_book)
print(type(clean_book))

text = gutenbergpy.textshow.get_text_by_id(1000)

with open('gutenbergpy_clean.txt', 'w', encoding="utf-8") as f:
    f.write(text)


def main():
    pizarra_vacia()
    bola_de_billar(12, 10000)
    done()
    return 0

# RUN

if __name__ == '__main__':
    main()