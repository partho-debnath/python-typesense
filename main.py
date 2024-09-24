import typesense
import json

client = typesense.Client(
    {
        "nodes": [
            {
                "host": "localhost",
                "port": "8108",  # For Typesense Cloud use 443
                "protocol": "http",  # For Typesense Cloud use https
            }
        ],
        "api_key": "xyz",
        "connection_timeout_seconds": 2,
    }
)


def create_schema():
    schema = {
        "name": "books",
        "fields": [
            {"name": "title", "type": "string", "index": True},
            {"name": "authors", "type": "string[]", "facet": True},
            {"name": "publication_year", "type": "int32", "facet": True},
            {"name": "ratings_count", "type": "int32"},
            {"name": "average_rating", "type": "float"},
        ],
        "default_sorting_field": "ratings_count",
    }

    response = client.collections.create(schema)
    print(response)


def upload_data():
    with open("books.jsonl", "r") as file_data:
        for i in file_data.readlines():
            client.collections["books"].documents.import_(i)


def add_data():
    data = {
        "title": "The First World War-2",
        "authors": ["John Keegan"],
        "publication_year": 1998,
        "id": "10001",
        "average_rating": 4,
        "image_url": "https://images.gr-assets.com/books/1403194704m/8914.jpg",
        "ratings_count": 9162,
    }
    client.collections["books"].documents.create(data)


def get_book_collection_config():
    data = client.collections["books"].retrieve()
    print(data)


def get_collections_config():
    data = client.collections.retrieve()
    print(json.dumps(data))


def delete_collection():
    client.collections["books"].delete()


def get_specific_document():
    data = client.collections["books"].documents["10001"].retrieve()
    print(data)
