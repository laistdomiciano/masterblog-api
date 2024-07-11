from flask import Flask, jsonify, request, flash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This is the third post."},
    {"id": 4, "title": "Fourth post", "content": "This is the fourth post."},
    {"id": 5, "title": "Fifth post", "content": "This is the fifth post."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
  sort_field = request.args.get('sort', 'id')
  direction = request.args.get('direction', 'asc')

  if sort_field not in ['id', 'title', 'content']:
    return jsonify({"error": "Invalid sort field"}), 400

  if direction not in ['asc', 'desc']:
    return jsonify({"error": "Invalid direction"}), 400

  sorted_posts = sorted(POSTS, key=lambda post: post[sort_field])
  if direction == 'desc':
    sorted_posts.reverse()

  return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
  post_to_delete = None
  for post in POSTS:
    if post['id'] == id:
      post_to_delete = post
      break

  if not post_to_delete:
    return jsonify({"message": f"Post with id {id} not found."}), 404

  POSTS.remove(post_to_delete)

  return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
  post_to_update = None
  for post in POSTS:
    if post['id'] == id:
      post_to_update = post
      break

  if not post_to_update:
    return jsonify({"message": f"Post with id {id} not found."}), 404

  data = request.get_json()

  if data and "title" in data:
    post_to_update["title"] = data["title"]
  if data and "content" in data:
    post_to_update["content"] = data["content"]

  return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
  title = request.args.get('title')
  content = request.args.get('content')

  filtered_posts = [post for post in POSTS if
                    (title and title.lower() in post['title'].lower()) or
                    (content and content.lower() in post['content'].lower())]

  return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)