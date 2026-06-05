import requests
from pymongo import MongoClient


API_URL = "https://api.disneyapi.dev/character"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "taller4_db"
COLLECTION_NAME = "raw.data"
MIN_RECORDS = 100


def descargar_personajes(min_records=MIN_RECORDS):
    personajes = []
    url = API_URL
    pagina = 1

    while url and len(personajes) < min_records:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        

        personajes.extend(data["data"])
        print(f"  Página {pagina}: {len(data['data'])} personajes (total: {len(personajes)})")
        pagina += 1
        url = data.get("info", {}).get("nextPage")

    if len(personajes) < min_records:
        raise ValueError(f"La API devolvio {len(personajes)} registros, menos del minimo requerido: {min_records}")

    return personajes[:min_records]


def guardar_en_mongodb(documentos):
    cliente = MongoClient(MONGO_URI)
    db = cliente[DB_NAME]
    coleccion = db[COLLECTION_NAME]

    coleccion.delete_many({})
    resultado = coleccion.insert_many(documentos)
    total = coleccion.count_documents({})

    cliente.close()
    return len(resultado.inserted_ids), total


def main():
    personajes = descargar_personajes()
    insertados, total = guardar_en_mongodb(personajes)

    print(f"Documentos descargados: {len(personajes)}")
    print(f"Documentos insertados: {insertados}")
    print(f"Documentos en MongoDB: {total}")
    print(f"Base de datos: {DB_NAME}")
    print(f"Coleccion: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()