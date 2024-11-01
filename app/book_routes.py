from flask import Blueprint, request, jsonify
from app import db
from .models import Book
from .schemas import BookSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

book_bp = Blueprint('books', __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@book_bp.route('/', methods=['GET'])
@jwt_required()
def list_books():
    books = Book.query.all()
    return jsonify(books_schema.dump(books)), 200

@book_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def retrieve_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book_schema.dump(book)), 200

@book_bp.route('/', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_book = Book(**data)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(book_schema.dump(new_book)), 201

@book_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    book.title = data['title']
    book.author = data['author']
    book.description = data.get('description')
    db.session.commit()

    return jsonify(book_schema.dump(book)), 200

@book_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"msg": "Book deleted"}), 204
