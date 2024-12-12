from flask import request, jsonify, redirect, url_for, session
import sqlite3
import hashlib

DB_PATH = 'encrypt.db'  

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def process_register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password or not confirm_password:
        return jsonify({"error": "Все поля обязательны"}), 400

    if len(password) < 6:
        return jsonify({"error": "Пароль должен быть не менее 6 символов"}), 400

    if password != confirm_password:
        return jsonify({"error": "Пароли не совпадают"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({"error": "Пользователь с таким логином уже существует"}), 400

        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()

        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]


        session['user_id'] = user_id

        return redirect(url_for('chat'))  
    except sqlite3.Error as e:
        return jsonify({"error": f"Ошибка базы данных: {e}"}), 500
    finally:
        conn.close()
