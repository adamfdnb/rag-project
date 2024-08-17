from typing import Dict, List, Union
import numpy as np
from elasticsearch import Elasticsearch


@data_loader
def search_documents(*args, **kwargs) -> List[Dict]:
    query = kwargs.get('query', "When is the next cohort?")
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', "documents_20240815_5306")
    top_k = kwargs.get('top_k', 5)
    course_filter = kwargs.get('course_filter', 'llm-zoomcamp')

    search_query = {
        "size": top_k,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": course_filter
                    }
                }
            }
        },
        "_source": ["question", "section", "course", "document_id"]
    }

    es_client = Elasticsearch(connection_string)

    response = es_client.search(
        index=index_name,
        body=search_query
    )

    if response["hits"]["hits"]:
        best_match_id = response["hits"]["hits"][0]["_source"]["document_id"]
        print("ID of the best matching result:", best_match_id)

    return [
        {
            "text": hit["_source"].get("text", ""),
            "question": hit["_source"].get("question", ""),
            "section": hit["_source"].get("section", ""),
            "course": hit["_source"].get("course", ""),
            "document_id": hit["_source"].get("document_id", "")
        }
        for hit in response["hits"]["hits"]
    ]