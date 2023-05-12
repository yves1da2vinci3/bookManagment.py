from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    year = db.Column(db.Integer)

    def __init__(self, title, author, genre, year):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'year': self.year
        }
with app.app_context():
    db.create_all()    
    
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book.serialize())
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    year = data.get('year')

    if not title or not author or not genre or not year:
        return jsonify({'error': 'Missing required fields'}), 400

    book = Book(title=title, author=author, genre=genre, year=year)
    db.session.add(book)
    db.session.commit()

    return jsonify(book.serialize()), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    year = data.get('year')

    if title:
        book.title = title
    if author:
        book.author = author
    if genre:
        book.genre = genre
    if year:
        book.year = year

    db.session.commit()

    return jsonify(book.serialize())

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)

