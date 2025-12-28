import requests
from faker import Faker
import random

fake = Faker()

BASE_URL = "http://127.0.0.1:8000"

NUM_SPECIES = 50
NUM_ENCLOSURES = 20
NUM_PLACEMENTS = 80  # Not more than NUM_SPECIES * NUM_ENCLOSURES

species_ids = []
enclosure_ids = []

animal_species = [
    "Panthera leo", "Elephas maximus", "Gorilla gorilla",
    "Canis lupus", "Felis catus", "Ursus arctos",
    "Ailuropoda melanoleuca", "Loxodonta africana", "Equus ferus",
    "Rhinoceros unicornis", "Haliaeetus leucocephalus", "Crocodylus niloticus",
    "Spheniscus demersus", "Pavo cristatus", "Struthio camelus"
]

# ----------- Species -----------
for _ in range(NUM_SPECIES):
    data = {
        "name": random.choice(animal_species) + "_" + str(random.randint(1, 10000)),
        "family": fake.word(),
        "habitat": fake.word(),
        "lifespan_years": random.randint(1, 50)
    }
    r = requests.post(f"{BASE_URL}/species", json=data)
    if r.status_code in [200, 201]:
        species_ids.append(r.json()["id"])
    else:
        print("Species error:", r.status_code, r.text)

# ----------- Enclosures -----------
for i in range(NUM_ENCLOSURES):
    data = {
        "room_number": i + 1,
        "complex_name": fake.word() + "_complex",
        "has_pond": random.choice([True, False]),
        "area": round(random.uniform(10.0, 500.0), 2)
    }
    r = requests.post(f"{BASE_URL}/enclosures", json=data)
    if r.status_code in [200, 201]:
        enclosure_ids.append(r.json()["id"])
    else:
        print("Enclosure error:", r.status_code, r.text)

# ----------- Placements -----------
used_pairs = set()

for _ in range(NUM_PLACEMENTS):
    if len(used_pairs) >= len(species_ids) * len(enclosure_ids):
        break

    species_id = random.choice(species_ids)
    enclosure_id = random.choice(enclosure_ids)

    # Generating unique pair
    while (species_id, enclosure_id) in used_pairs:
        species_id = random.choice(species_ids)
        enclosure_id = random.choice(enclosure_ids)

    used_pairs.add((species_id, enclosure_id))

    data = {
        "species_id": species_id,
        "enclosure_id": enclosure_id,
        "animals_count": random.randint(1, 20)
    }
    r = requests.post(f"{BASE_URL}/placements", json=data)
    if r.status_code not in [200, 201]:
        print("Placement error:", r.status_code, r.text)

print("Database populated ✅")
