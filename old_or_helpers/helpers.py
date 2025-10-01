def preview_vector(index, vector_id, namespace="default", num_values=10):
    response = index.fetch(ids=[vector_id], namespace=namespace)

    # response.vectors is a dict {id: Vector}
    if vector_id not in response.vectors:
        print(f"Vector {vector_id} not found in namespace '{namespace}'")
        return

    vector_data = response.vectors[vector_id]

    print(f"📌 ID: {vector_id}")
    print(f"Metadata: {vector_data.metadata}")
    values = vector_data.values
    print(f"Values preview: {values[:num_values]} ... (showing {num_values} of {len(values)})")
