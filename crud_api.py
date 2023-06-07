from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL database configuration
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Satyam@98',
    'database': 'movies'
}

# Create MySQL connection
conn = mysql.connector.connect(**config)
cursor = conn.cursor()


# Create API for adding data (POST)
@app.route('/blog/create', methods=['POST'])
def create_blog():
    # id = request.json['id']
    title = request.json['title']
    author = request.json['author']
    body = request.json['body']
    date = request.json['date']

    # Prepare the SQL query
    query = "INSERT INTO user (title, author, body, date) VALUES ( %s, %s, %s, %s)"
    values = (title, author, body, date)

    try:
        # Execute the query
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Data added successfully.'}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred while add data.'}), 500

# Create API for getting single data (GET)
@app.route('/blog/<int:id>', methods=['GET'])
def get_blog(id):
    # Prepare the SQL query
    query = "SELECT * FROM user WHERE id = %s"
    values = (id,)

    try:
        # Execute the query
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            blog = {
                'id': result[0],
                'title': result[1],
                'author': result[2],
                'body': result[3],
                'date': result[4].strftime('%Y-%m-%d')
            }
            return jsonify(blog), 200
        else:
            return jsonify({'message': 'data not found.'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred while fetching data.'}), 500
# Create API for getting all data (GET)
@app.route('/blog', methods=['GET'])
def get_all_blogs():
    # Prepare the SQL query
    query = "SELECT * FROM user"

    try:
        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()

        blogs = []
        for result in results:
            blog = {
                'id': result[0],
                'title': result[1],
                'author': result[2],
                'body': result[3],
                'date': result[4].strftime('%Y-%m-%d')
            }
            blogs.append(blog)

        return jsonify(blogs), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred while fetching data.'}), 500
# Create API for updating data by id (PUT)
@app.route('/blog/<int:id>', methods=['PUT'])
def update_blog(id):
    # Check if the blog exists
    check_query = "SELECT * FROM user WHERE id = %s"
    check_values = (id,)
    cursor.execute(check_query, check_values)
    result = cursor.fetchone()
    
    if not result:
        return jsonify({'message': 'data not found.'}), 404

    # Extract the updated values from the request body
    title = request.json.get('title', result[1])
    author = request.json.get('author', result[2])
    body = request.json.get('body', result[3])
    date = request.json.get('date', result[4].strftime('%Y-%m-%d'))

    # Prepare the SQL query
    query = "UPDATE user SET title = %s, author = %s, body = %s, date = %s WHERE id = %s"
    values = (title, author, body, date, id)

    try:
        # Execute the query
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'data updated successfully.'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred while updating data.'}), 500



# Create API for deleting data by id (DELETE)
@app.route('/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    # Check if the blog exists
    check_query = "SELECT * FROM user WHERE id = %s"
    check_values = (id,)
    cursor.execute(check_query, check_values)
    result = cursor.fetchone()

    if not result:
        return jsonify({'message': 'data not found.'}), 404

    # Prepare the SQL query
    query = "DELETE FROM user WHERE id = %s"
    values = (id,)

    try:
        # Execute the query
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'data deleted successfully.'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error occurred while deleting data.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8000)
