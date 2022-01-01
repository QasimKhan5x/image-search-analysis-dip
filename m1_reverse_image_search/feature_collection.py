import time

from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)


def setup_collection(collection_name="voc2012_ris"):
    dim = 512
    default_fields = [
        FieldSchema(name="id", dtype=DataType.INT64,
                    is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    default_schema = CollectionSchema(
        fields=default_fields, description="PASCAL VOC 2012 collection")

    collection = Collection(name=collection_name, schema=default_schema)
    return collection


def get_collection(collection_name="voc2012_ris"):
    '''Assumes that a connection to milvus has been established'''
    assert utility.has_collection(collection_name), \
        "ERROR: Collection not found"
    collection = Collection(collection_name)
    return collection


def search_collection(collection, vectors, topK):
    search_params = {"metric_type": "L2"}
    if not isinstance(vectors, list):
        vectors = vectors.tolist()
    print("Searching collection...")
    start = time.time()
    res = collection.search(data=vectors,
                            anns_field="vector",
                            param=search_params,
                            limit=topK)
    end = time.time() - start
    print(f"Search took {end} seconds")
    return res


if __name__ == '__main__':
    # connect to Milvus
    connections.connect(host="127.0.0.1", port=19530)
    # Create or Get a collection
    if utility.has_collection("voc2012_ris"):
        print("Collection Found!")
        collection = get_collection("voc2012_ris")

    else:
        print("Collection not found. Creating.")
        collection = setup_collection()
    connections.disconnect("default")
    print("SUCCESS")
