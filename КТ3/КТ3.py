from toolz import compose, curry

# 1 задание

def read_books(books):
  with open(books, 'r', encoding='utf-8') as f:
    data = f.read()
  return data.split('\n')

def split_books_properties(books):
  books_list = [x.split('|') for x in books if x]
  return books_list[1:]

def change_types(books):
  return list(map(lambda a: a[:-2] + [int(a[3]), float(a[4])], books))

get_books = compose(change_types, split_books_properties, read_books)


# 2 задание

@curry
def search_books(search, books):
  return list(filter(lambda x: search.lower() in x[1].lower(), books))

def concat_books_authors(books):
  return list(map(lambda x:[ x[0], f'{x[1]}, {x[2]}'] + x[3:], books))

filtered_books = compose(concat_books_authors, search_books('python'), get_books)


# 3 задание
def revenue(books):
  return list(map(lambda x: tuple([x[0], round(x[2]*x[3], 2)]), books))

final_function = compose(revenue, filtered_books)