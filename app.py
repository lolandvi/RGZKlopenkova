from flask import Blueprint, Flask, render_template, redirect, request, url_for, jsonify, session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Простые списки для хранения имен пользователей и их хешированных паролей
usernames = []
password_hashes = []

# Список для хранения инициатив
initiatives = []

@app.route("/mainpage")
def mainpage():
    return render_template('mainpage.html')

@app.route('/initiatives', methods=['GET'])
def get_initiatives():
    # Возвращает список инициатив в формате JSON
    return jsonify(initiatives)

@app.route('/initiatives/delete', methods=['DELETE'])
def delete_last_initiative():
    # Удаление последней инициативы
    if initiatives:
        deleted_initiative = initiatives.pop()
        return jsonify({"success": True, "message": "Инициатива успешно удалена", "deleted_initiative": deleted_initiative})
    else:
        return jsonify({"success": False, "message": "Нет доступных инициатив для удаления"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Обработка данных формы входа
        username = request.form['username']
        password = request.form['password']

        # Проверка логина и пароля пользователя
        if username in usernames and bcrypt.check_password_hash(password_hashes[usernames.index(username)], password):
            # Успешная аутентификация, сохраняем информацию о пользователе в сессии
            session['username'] = username
            return redirect(url_for('mainpage'))
        else:
            error_message = "Аккаунт не найден. Перепроверьте корректность данных или создайте аккаунт"
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Обработка данных формы регистрации
        username = request.form['username']
        password = request.form['password']

        # Хеширование пароля перед сохранением
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Добавление пользователя в списки
        usernames.append(username)
        password_hashes.append(hashed_password)

        return redirect(url_for('login'))  # Перенаправление на страницу входа после успешной регистрации

    return render_template('register.html')

@app.route('/check_login', methods=['POST'])
def check_login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        if username in usernames and bcrypt.check_password_hash(password_hashes[usernames.index(username)], password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Аккаунт не найден. Перепроверьте корректность данных или создайте аккаунт'})

if __name__ == '__main__':
    app.run(debug=True)