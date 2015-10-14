import pprint

def raj_template_dump():
    dump_array = [{
        "type": "movies",
        "modes": [
            "top250",
            "random",
            "list all movies",
            "my fav movies"
        ]
    }, {
        "type": "books",
        "modes": [
            "popular",
            "random",
            "list all books",
            "my fav movies"
        ]
    }, {
        "type": "series",
        "modes": [
            "top250_tv",
            "random",
            "list all series",
            "horrible shows"
        ]
    }
    ]

    for i, enum in enumerate(dump_array):
        # pprint.pprint(dump_array)
        print dump_array[i]

raj_template_dump()
