def init_music() -> list:
    d = [
    ('Hendrix' , '1942'),
    ('Allman' , '1946'),
    ('King' , '1925'),
    ('Clapton' , '1945'),
    ('Johnson' , '1911'),
    ('Berry' , '1926'),
    ('Vaughan' , '1954'),
    ('Cooder' , '1947'),
    ('Page' , '1944'),
    ('Richards' , '1943'),
    ('Hammett' , '1962'),
    ('Cobain' , '1967'),
    ('Garcia' , '1942'),
    ('Beck' , '1944'),
    ('Santana' , '1947'),
    ('Ramone' , '1948'),
    ('White' , '1975'),
    ('Frusciante', '1970'),
    ('Thompson' , '1949'),
    ('Burton' , '1939')
    ]
    return d

def sort_by_year(d: list) -> dict:
    result = dict()
    for title, year in d:
        if year in result:
            result[year].append(title)
        else:
            result[year] = [title]
    return result

if __name__ == "__main__":
    music_list = init_music()
    music_dict = sort_by_year(music_list)
    for year, titles in music_dict.items():
        print(f"{year} : {' '.join(titles)}")