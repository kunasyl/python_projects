import collections

data = {
    "id": 1,
    "first_name": "Jonathan",
    "last_name": "Hsu",
    "employment_history": [
        {
            "company": "Black Belt Academy",
            "title": "Instructor",
            "something": {
                "hello": [1,2,3,{
                    "something":"goes"
                }]
            }
        },
        {
            "company": "Zerion Software",
            "title": "Solutions Engineer"
        }
    ],
    "education": {
        "bachelors": "Information Technology",
        "masters": "Applied Information Technology",
        "phd": "Higher Education"
    }
}


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for k, v in enumerate(v):
                items.extend(flatten({str(k): v}, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

             
ready_data = flatten(data)

for k,v in ready_data.items():
    print(k + ':' + str(v))