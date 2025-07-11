# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List

from google.cloud import aiplatform


#  [START aiplatform_sdk_vector_search_find_neighbors_sample]
def vector_search_find_neighbors(
    project: str,
    location: str,
    index_endpoint_name: str,
    deployed_index_id: str,
    queries: List[List[float]],
    num_neighbors: int,
) -> List[
    List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]
]:
    """Query the vector search index.

    Args:
        project (str): Required. Project ID
        location (str): Required. The region name
        index_endpoint_name (str): Required. Index endpoint to run the query
        against.
        deployed_index_id (str): Required. The ID of the DeployedIndex to run
        the queries against.
        queries (List[List[float]]): Required. A list of queries. Each query is
        a list of floats, representing a single embedding.
        num_neighbors (int): Required. The number of neighbors to return.

    Returns:
        List[List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]] - A list of nearest neighbors for each query.
    """
    # Initialize the Vertex AI client
    aiplatform.init(project=project, location=location)

    # Create the index endpoint instance from an existing endpoint.
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=index_endpoint_name
    )

    # Query the index endpoint for the nearest neighbors.
    return my_index_endpoint.find_neighbors(
        deployed_index_id=deployed_index_id,
        queries=queries,
        num_neighbors=num_neighbors,
    )


#  [END aiplatform_sdk_vector_search_find_neighbors_sample]


#  [START aiplatform_sdk_vector_search_find_neighbors_hybrid_sample]
def vector_search_find_neighbors_hybrid_queries(
    project: str,
    location: str,
    index_endpoint_name: str,
    deployed_index_id: str,
    num_neighbors: int,
) -> List[
    List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]
]:
    """Query the vector search index using example hybrid queries.

    Args:
        project (str): Required. Project ID
        location (str): Required. The region name
        index_endpoint_name (str): Required. Index endpoint to run the query
        against.
        deployed_index_id (str): Required. The ID of the DeployedIndex to run
        the queries against.
        num_neighbors (int): Required. The number of neighbors to return.

    Returns:
        List[List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]] - A list of nearest neighbors for each query.
    """
    # Initialize the Vertex AI client
    aiplatform.init(project=project, location=location)

    # Create the index endpoint instance from an existing endpoint.
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=index_endpoint_name
    )

    # Query hybrid datapoints, sparse-only datapoints, and dense-only datapoints.
    hybrid_queries = [
        aiplatform.matching_engine.matching_engine_index_endpoint.HybridQuery(
            dense_embedding=[1, 2, 3],
            sparse_embedding_dimensions=[10, 20, 30],
            sparse_embedding_values=[1.0, 1.0, 1.0],
            rrf_ranking_alpha=0.5,
        ),
        aiplatform.matching_engine.matching_engine_index_endpoint.HybridQuery(
            dense_embedding=[1, 2, 3],
            sparse_embedding_dimensions=[10, 20, 30],
            sparse_embedding_values=[0.1, 0.2, 0.3],
        ),
        aiplatform.matching_engine.matching_engine_index_endpoint.HybridQuery(
            sparse_embedding_dimensions=[10, 20, 30],
            sparse_embedding_values=[0.1, 0.2, 0.3],
        ),
        aiplatform.matching_engine.matching_engine_index_endpoint.HybridQuery(
            dense_embedding=[1, 2, 3]
        ),
    ]

    return my_index_endpoint.find_neighbors(
        deployed_index_id=deployed_index_id,
        queries=hybrid_queries,
        num_neighbors=num_neighbors,
    )


#  [END aiplatform_sdk_vector_search_find_neighbors_hybrid_sample]


#  [START aiplatform_sdk_vector_search_find_neighbors_filtering_crowding_sample]
def vector_search_find_neighbors_filtering_crowding(
    project: str,
    location: str,
    index_endpoint_name: str,
    deployed_index_id: str,
    queries: List[List[float]],
    num_neighbors: int,
    filter: List[aiplatform.matching_engine.matching_engine_index_endpoint.Namespace],
    numeric_filter: List[
        aiplatform.matching_engine.matching_engine_index_endpoint.NumericNamespace
    ],
    per_crowding_attribute_neighbor_count: int,
) -> List[
    List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]
]:
    """Query the vector search index with filtering and crowding.

    Args:
        project (str): Required. Project ID
        location (str): Required. The region name
        index_endpoint_name (str): Required. Index endpoint to run the query
        against.
        deployed_index_id (str): Required. The ID of the DeployedIndex to run
        the queries against.
        queries (List[List[float]]): Required. A list of queries. Each query is
        a list of floats, representing a single embedding.
        num_neighbors (int): Required. The number of neighbors to return.
        filter (List[Namespace]): Required. A list of Namespaces for filtering
        the matching results. For example,
        [Namespace("color", ["red"], []), Namespace("shape", [], ["square"])]
        will match datapoints that satisfy "red color" but not include
        datapoints with "square shape".
        numeric_filter (List[NumericNamespace]): Required. A list of
        NumericNamespaces for filtering the matching results. For example,
        [NumericNamespace(name="cost", value_int=5, op="GREATER")] will limit
        the matching results to datapoints with cost greater than 5.
        per_crowding_attribute_neighbor_count (int): Required. The maximum
        number of returned matches with the same crowding tag.

    Returns:
        List[List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]] - A list of nearest neighbors for each query.
    """
    # Initialize the Vertex AI client
    aiplatform.init(project=project, location=location)

    # Create the index endpoint instance from an existing endpoint.
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=index_endpoint_name
    )

    # Query the index endpoint for the nearest neighbors.
    return my_index_endpoint.find_neighbors(
        deployed_index_id=deployed_index_id,
        queries=queries,
        num_neighbors=num_neighbors,
        filter=filter,
        numeric_filter=numeric_filter,
        per_crowding_attribute_neighbor_count=per_crowding_attribute_neighbor_count,
    )


#  [END aiplatform_sdk_vector_search_find_neighbors_filtering_crowding_sample]


#  [START aiplatform_sdk_vector_search_find_neighbors_jwt_sample]
def vector_search_find_neighbors_jwt(
    project: str,
    location: str,
    index_endpoint_name: str,
    deployed_index_id: str,
    queries: List[List[float]],
    num_neighbors: int,
    signed_jwt: str,
) -> List[
    List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]
]:
    """Query the vector search index.

    Args:
        project (str): Required. Project ID
        location (str): Required. The region name
        index_endpoint_name (str): Required. Index endpoint to run the query
        against.
        deployed_index_id (str): Required. The ID of the DeployedIndex to run
        the queries against.
        queries (List[List[float]]): Required. A list of queries. Each query is
        a list of floats, representing a single embedding.
        num_neighbors (int): Required. The number of neighbors to return.
        signed_jwt (str): Required. The signed JWT token for the private
        endpoint. The endpoint must be configured to accept tokens from JWT's
        issuer and encoded audience.

    Returns:
        List[List[aiplatform.matching_engine.matching_engine_index_endpoint.MatchNeighbor]] - A list of nearest neighbors for each query.
    """
    # Initialize the Vertex AI client
    aiplatform.init(project=project, location=location)

    # Create the index endpoint instance from an existing endpoint.
    my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=index_endpoint_name
    )

    # Query the index endpoint for the nearest neighbors.
    resp = my_index_endpoint.find_neighbors(
        deployed_index_id=deployed_index_id,
        queries=queries,
        num_neighbors=num_neighbors,
        signed_jwt=signed_jwt,
    )
    return resp


#  [END aiplatform_sdk_vector_search_find_neighbors_jwt_sample]
