from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    '''
    Route to get all posts with optional sorting and direction
    :return: Error if sort or direction is invalid, sorted posts otherwise
    '''
    sort = request.args.get('sort') or None
    direction = request.args.get('direction') or 'asc'

    if sort and sort not in ('title', 'content'):
        return jsonify({"error": "sort must be 'title' or 'content'."}), 400
    if direction not in ('asc', 'desc'):
        return jsonify({"error": "direction must be 'asc' or 'desc'."}), 400

    posts = sorted(
        POSTS, key=lambda p: p[sort].lower(), reverse=(direction == 'desc')
    ) if sort else POSTS
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def create_posts():
    '''
    Creates a new post with given title and content
    :return: Error if title or content is missing, new post otherwise
    '''
    data = request.get_json()
    if not data or not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content are required."}), 400

    new_id = max((p["id"] for p in POSTS), default=0) + 1
    post = {"id": new_id, "title": data["title"], "content": data["content"]}
    POSTS.append(post)
    return jsonify(post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Deletes a post based on the provided post ID.
    The function looks for a post with a matching ID
    and removes it from the list.
    If no post is found with the given ID, an error response is
    returned with a 404 status code.

    :param post_id: The ID of the post to be deleted
    :type post_id: int
    :return: A JSON representation of the deleted post or an error message if the post is not found
    """
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    POSTS.remove(post)
    return jsonify(post), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Updates an existing post by its unique `post_id`.
    The function looks for a post with given `post_id`
    within the predefined `POSTS` list.
    If the post is found, its title and/or content are updated using
    the provided JSON payload from the request body.
    If no matching post is found, an error message is
    returned with a status of `404`.

    :param post_id: The unique identifier of the post to be updated.
    :type post_id: int

    :return: JSON-formatted response that includes the updated post if successful,
        or an error message if the post is not found. The HTTP status code is 200
        on success and 404 if the post was not found.
    """
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404

    data = request.get_json()
    if data and (data.get("title") or data.get("content")):
        post["title"] = data.get("title", post["title"])
        post["content"] = data.get("content", post["content"])

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Handles the search functionality for posts.
    This endpoint allows users to search for posts
    using a query parameter 'title'.
    The search is case-insensitive and matches
    all posts containing the given query string in their titles.

    Raises 400 Bad Request error code if the required query parameter 'title' is
    not provided.

    :returns: JSON response containing a list of search results (posts that match
        the search query) or an error message if the query parameter is missing.
    """
    query = request.args.get('title')
    if not query:
        return jsonify({"error": "Query parameter 'title' is required."}), 400

    results = [p for p in POSTS if query.lower() in p["title"].lower()]
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
