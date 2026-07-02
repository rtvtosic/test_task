from config import client

# ==== создание индекса ====
def create_index():
    mappings = {
        "properties": {
            "id": {"type": "integer"},
            "text": {"type": "text"}
        }
    }

    # client.indices.delete(index="documents")

    if not client.indices.exists(index="documents"):
        client.indices.create(index="documents", mappings=mappings)


if __name__ == "__main__":
    create_index()