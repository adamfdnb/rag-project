from typing import Dict, List

from elasticsearch import Elasticsearch, exceptions

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_loader
def search_query(*args, **kwargs) -> str:
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')
    search_fields = kwargs.get('search_fields', ['title', 'content'])
    query = "When is the next cohort?"

    es_client = Elasticsearch(connection_string)

    try:
        response = es_client.search(
            index=index_name,
            body={
                "size": 1,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": search_fields
                    }
                },
            },
        )

        print("Raw response from Elasticsearch:", response)

        if response['hits']['hits']:
            document_id = response['hits']['hits'][0]['_id']
            print(f"Top matching document ID: {document_id}")
            return document_id
        else:
            print("No matching documents found.")
            return "No matching documents found."

    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return "Error occurred during search."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Error occurred during search."