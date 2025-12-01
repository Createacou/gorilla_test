import json
data = {
    "squadName": "Super hero squad",
    "homeTown": "Metro City",
    "formed": 2016,
    "secretBase": "Super tower",
    "active": True,
    "members": [
        {
            "name": "Molecule Man",
            "age": 29,
            "secretIdentity": "Dan Jukes",
            "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
        },
        {
            "name": "Madame Uppercut",
            "age": 39,
            "secretIdentity": "Jane Wilson",
            "powers": [
                "Million tonne punch",
                "Damage resistance",
                "Superhuman reflexes"
            ]
        },
        {
            "name": "Eternal Flame",
            "age": 1000000,
            "secretIdentity": "Unknown",
            "powers": [
                "Immortality",
                "Heat Immunity",
                "Inferno",
                "Teleportation",
                "Interdimensional travel"
            ]
        }
    ]
}

new_heroes = [
    {
        "name": "Super Dick",
        "age": 33,
        "secretIdentity": "mihail Crug",
        "powers": ["Slavuanskii zazhim yaikami", "Super Punch", "Energy shield"]
    },
    {
        "name": "MegaBrain",
        "age": 35,
        "secretIdentity": "Dr.Barmental",
        "powers": ["Mindstorm", "Math", "Stealth mode"]
    }
]

data["members"].extend(new_heroes)

data["members"].sort(key=lambda hero: hero["age"])

with open("superhero_new.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Файл superhero_new.json успешно создан с отсортированными супергероями.")