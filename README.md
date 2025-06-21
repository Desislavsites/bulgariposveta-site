from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import json
import os
import random
import string
from datetime import datetime, timedelta
from dotenv import load_dotenv
from simple_email import send_verification_email_simple

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'bulgarians-world-secret-key')
CORS(app, origins="*")

# Simple file-based storage
USERS_FILE = 'users.json'
PENDING_USERS_FILE = 'pending_users.json'

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code):
    """Send verification email using the working simple email function"""
    return send_verification_email_simple(email, code)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def load_pending_users():
    if os.path.exists(PENDING_USERS_FILE):
        try:
            with open(PENDING_USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_users(pending_users):
    try:
        with open(PENDING_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(pending_users, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving pending users: {e}")
        return False

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Българи по Света - Общност на българите по света</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background: linear-gradient(135deg, 
                #ffffff 0%, 
                #f7fafc 25%, 
                #edf2f7 50%, 
                #e2e8f0 75%, 
                #cbd5e0 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }

        /* Български орнаменти като фон */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(220, 38, 127, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(56, 178, 172, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 60%, rgba(245, 101, 101, 0.05) 0%, transparent 50%);
            z-index: -1;
        }

        /* Навигация с български акценти */
        .navbar {
            background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
            backdrop-filter: blur(10px);
            border-bottom: 3px solid #dc267f;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(220, 38, 127, 0.1);
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: #2d3748;
            text-decoration: none;
            background: linear-gradient(135deg, #dc267f, #38b2ac);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .logo::before {
            content: '🌹';
            margin-right: 0.5rem;
            font-size: 1.8rem;
        }

        .nav-buttons {
            display: flex;
            gap: 1rem;
        }

        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.95rem;
        }

        .btn-primary {
            background: linear-gradient(135deg, #dc267f, #f56565);
            color: white;
            box-shadow: 0 4px 15px rgba(220, 38, 127, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(220, 38, 127, 0.4);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #38b2ac, #4fd1c7);
            color: white;
            box-shadow: 0 4px 15px rgba(56, 178, 172, 0.3);
        }

        .btn-secondary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(56, 178, 172, 0.4);
        }

        /* Hero секция с български мотиви */
        .hero {
            text-align: center;
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -50px;
            left: 50%;
            transform: translateX(-50%);
            width: 200px;
            height: 4px;
            background: linear-gradient(90deg, #dc267f, #38b2ac, #f56565);
            border-radius: 2px;
        }

        .hero h1 {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, #2d3748, #4a5568);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.2;
        }

        .hero p {
            font-size: 1.25rem;
            color: #4a5568;
            margin-bottom: 3rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }

        .hero-buttons {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 4rem;
        }

        .btn-hero {
            padding: 1rem 2rem;
            font-size: 1.1rem;
            border-radius: 15px;
            font-weight: 600;
            min-width: 200px;
        }

        /* Статистики с български цветове */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin: 4rem 0;
            padding: 0 2rem;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }

        .stat-card {
            background: linear-gradient(135deg, #ffffff, #f7fafc);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 2px solid transparent;
            background-clip: padding-box;
            position: relative;
            transition: all 0.3s ease;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 20px;
            padding: 2px;
            background: linear-gradient(135deg, #dc267f, #38b2ac, #f56565);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: exclude;
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #dc267f, #f56565);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: #4a5568;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
        }

        /* Секции с услуги */
        .services {
            padding: 4rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .service-card {
            background: linear-gradient(135deg, #ffffff, #f7fafc);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
        }

        .service-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 20px;
            padding: 2px;
            background: linear-gradient(135deg, #dc267f, #38b2ac);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: exclude;
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .service-card:hover::before {
            opacity: 1;
        }

        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .service-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            display: block;
        }

        .service-card h3 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2d3748;
        }

        .service-card p {
            color: #4a5568;
            line-height: 1.6;
        }

        /* Модали с български стил */
        .modal {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            background: linear-gradient(135deg, #ffffff, #f7fafc);
            margin: 5% auto;
            padding: 2.5rem;
            border-radius: 20px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
            position: relative;
            border: 3px solid transparent;
            background-clip: padding-box;
        }

        .modal-content::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 20px;
            padding: 3px;
            background: linear-gradient(135deg, #dc267f, #38b2ac, #f56565);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: exclude;
            mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            mask-composite: exclude;
        }

        .close {
            color: #a0aec0;
            float: right;
            font-size: 2rem;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .close:hover {
            color: #dc267f;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #2d3748;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #ffffff;
        }

        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #dc267f;
            box-shadow: 0 0 0 3px rgba(220, 38, 127, 0.1);
        }

        /* Responsive дизайн */
        @media (max-width: 768px) {
            .nav-container {
                padding: 0 1rem;
            }

            .hero {
                padding: 2rem 1rem;
            }

            .hero-buttons {
                flex-direction: column;
                align-items: center;
            }

            .btn-hero {
                width: 100%;
                max-width: 300px;
            }

            .stats {
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
                padding: 0 1rem;
            }

            .services-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }

            .modal-content {
                margin: 10% auto;
                padding: 2rem;
            }
        }

        @media (max-width: 480px) {
            .stats {
                grid-template-columns: 1fr;
            }

            .nav-buttons {
                flex-direction: column;
                gap: 0.5rem;
            }

            .btn {
                padding: 0.6rem 1.2rem;
                font-size: 0.9rem;
            }
        }

        /* Анимации */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .hero h1,
        .hero p,
        .service-card,
        .stat-card {
            animation: fadeInUp 0.6s ease-out;
        }

        .service-card:nth-child(2) {
            animation-delay: 0.1s;
        }

        .service-card:nth-child(3) {
            animation-delay: 0.2s;
        }

        /* Допълнителни български акценти */
        .bulgarian-pattern {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 2rem;
            opacity: 0.1;
            color: #dc267f;
        }

        .footer-pattern {
            text-align: center;
            padding: 2rem;
            color: #a0aec0;
            font-size: 0.9rem;
        }

        .footer-pattern::before {
            content: '🌹 ❀ 🌹 ❀ 🌹';
            display: block;
            margin-bottom: 1rem;
            font-size: 1.5rem;
            opacity: 0.3;
        }
    </style>
</head>
<body>
    <div class="bulgarian-pattern">❀</div>
    
    <!-- Навигация -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="#" class="logo">Българи по Света</a>
            <div class="nav-buttons">
                <button class="btn btn-secondary" onclick="openModal('loginModal')">Вход</button>
                <button class="btn btn-primary" onclick="openModal('registerModal')">Регистрация</button>
            </div>
        </div>
    </nav>

    <!-- Hero секция -->
    <section class="hero">
        <h1>Добре дошли в общността на българите по света!</h1>
        <p>Свържете се с българи от цял свят. Намерете работа, жилище или услуги. Споделете своя опит и помогнете на други.</p>
        
        <div class="hero-buttons">
            <button class="btn btn-primary btn-hero" onclick="openModal('registerModal')">
                🌹 Присъединете се сега
            </button>
            <button class="btn btn-secondary btn-hero" onclick="scrollToServices()">
                🚀 Разгледайте услугите
            </button>
        </div>

        <!-- Статистики -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">1000+</div>
                <div class="stat-label">Членове</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">50+</div>
                <div class="stat-label">Страни</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">500+</div>
                <div class="stat-label">Обяви</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Поддръжка</div>
            </div>
        </div>
    </section>

    <!-- Услуги -->
    <section class="services" id="services">
        <div class="services-grid">
            <div class="service-card">
                <span class="service-icon">💼</span>
                <h3>Работа</h3>
                <p>Намерете работни възможности или предложете работа на други българи по света. Свържете се с професионалисти във вашата област.</p>
            </div>
            <div class="service-card">
                <span class="service-icon">🏠</span>
                <h3>Жилища</h3>
                <p>Търсете или предлагайте жилища за наем или продажба в различни страни. Намерете перфектния дом за вас и вашето семейство.</p>
            </div>
            <div class="service-card">
                <span class="service-icon">🛠️</span>
                <h3>Услуги</h3>
                <p>Предлагайте или търсете различни услуги от българската общност. От ремонти до консултации - всичко на едно място.</p>
            </div>
        </div>
    </section>

    <div class="footer-pattern">
        Създадено с любов за българската общност по света
    </div>

    <!-- Модал за вход -->
    <div id="loginModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('loginModal')">&times;</span>
            <h2 style="margin-bottom: 2rem; color: #2d3748; text-align: center;">🌹 Вход</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" name="email" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Парола:</label>
                    <input type="password" id="loginPassword" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Влезте</button>
            </form>
        </div>
    </div>

    <!-- Модал за регистрация -->
    <div id="registerModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('registerModal')">&times;</span>
            <h2 style="margin-bottom: 2rem; color: #2d3748; text-align: center;">🌹 Регистрация</h2>
            <form id="registerForm">
                <div class="form-group">
                    <label for="firstName">Име:</label>
                    <input type="text" id="firstName" name="firstName" required>
                </div>
                <div class="form-group">
                    <label for="middleName">Презиме (по избор):</label>
                    <input type="text" id="middleName" name="middleName">
                </div>
                <div class="form-group">
                    <label for="lastName">Фамилия:</label>
                    <input type="text" id="lastName" name="lastName" required>
                </div>
                <div class="form-group">
                    <label for="username">Потребителско име:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Парола:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="birthDate">Дата на раждане:</label>
                    <input type="date" id="birthDate" name="birthDate" required>
                </div>
                <div class="form-group">
                    <label for="country">Държава на пребиваване:</label>
                    <select id="country" name="country" required>
                        <option value="">Изберете държава...</option>
                        <option value="България">България</option>
                        <option value="Германия">Германия</option>
                        <option value="Великобритания">Великобритания</option>
                        <option value="САЩ">САЩ</option>
                        <option value="Канада">Канада</option>
                        <option value="Австралия">Австралия</option>
                        <option value="Франция">Франция</option>
                        <option value="Италия">Италия</option>
                        <option value="Испания">Испания</option>
                        <option value="Нидерландия">Нидерландия</option>
                        <option value="Белгия">Белгия</option>
                        <option value="Швейцария">Швейцария</option>
                        <option value="Австрия">Австрия</option>
                        <option value="Друга">Друга</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Регистрирай се</button>
            </form>
        </div>
    </div>

    <!-- Модал за верификация -->
    <div id="verificationModal" class="modal">
        <div class="modal-content">
            <h2 style="margin-bottom: 2rem; color: #2d3748; text-align: center;">🌹 Потвърждение на email</h2>
            <p style="text-align: center; margin-bottom: 2rem; color: #4a5568;">
                Изпратихме ви код за потвърждение на вашия email адрес.
            </p>
            <form id="verificationForm">
                <div class="form-group">
                    <label for="verificationCode">Код за верификация:</label>
                    <input type="text" id="verificationCode" name="code" placeholder="Въведете 6-цифрения код" maxlength="6" required>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Потвърди</button>
            </form>
        </div>
    </div>

    <script>
        // Модални функции
        function openModal(modalId) {
            document.getElementById(modalId).style.display = 'block';
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        function scrollToServices() {
            document.getElementById('services').scrollIntoView({ behavior: 'smooth' });
        }

        // Затваряне на модал при клик извън него
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }

        // Регистрация
        document.getElementById('registerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeModal('registerModal');
                    openModal('verificationModal');
                    alert('Регистрацията е успешна! Проверете вашия email за код за потвърждение.');
                } else {
                    alert('Грешка: ' + result.message);
                }
            } catch (error) {
                alert('Възникна грешка при регистрацията');
            }
        });

        // Верификация
        document.getElementById('verificationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/verify', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeModal('verificationModal');
                    alert('Акаунтът ви е потвърден успешно! Добре дошли в общността!');
                    location.reload();
                } else {
                    alert('Грешка: ' + result.message);
                }
            } catch (error) {
                alert('Възникна грешка при верификацията');
            }
        });

        // Вход
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    closeModal('loginModal');
                    alert('Успешен вход! Добре дошли обратно!');
                    location.reload();
                } else {
                    alert('Грешка: ' + result.message);
                }
            } catch (error) {
                alert('Възникна грешка при влизането');
            }
        });
    </script>
</body>
</html>
    ''')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'username', 'email', 'password', 'birthDate', 'country']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Полето {field} е задължително'})
        
        # Check if user already exists
        users = load_users()
        for user in users:
            if user['email'] == data['email']:
                return jsonify({'success': False, 'message': 'Потребител с този email вече съществува'})
            if user['username'] == data['username']:
                return jsonify({'success': False, 'message': 'Потребителското име вече е заето'})
        
        # Generate verification code
        verification_code = generate_verification_code()
        
        # Store pending user
        pending_users = load_pending_users()
        pending_users[data['email']] = {
            'user_data': data,
            'verification_code': verification_code,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        if not save_pending_users(pending_users):
            return jsonify({'success': False, 'message': 'Грешка при запазване на данните'})
        
        # Send verification email
        if send_verification_email(data['email'], verification_code):
            return jsonify({'success': True, 'message': 'Регистрацията е успешна! Проверете вашия email.'})
        else:
            return jsonify({'success': False, 'message': 'Грешка при изпращане на email'})
            
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'Възникна грешка при регистрацията'})

@app.route('/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        code = data.get('code')
        
        if not code:
            return jsonify({'success': False, 'message': 'Кодът е задължителен'})
        
        pending_users = load_pending_users()
        
        # Find user by verification code
        user_email = None
        for email, pending_data in pending_users.items():
            if pending_data['verification_code'] == code:
                # Check if code is expired
                expires_at = datetime.fromisoformat(pending_data['expires_at'])
                if datetime.now() > expires_at:
                    return jsonify({'success': False, 'message': 'Кодът е изтекъл'})
                
                user_email = email
                break
        
        if not user_email:
            return jsonify({'success': False, 'message': 'Невалиден код'})
        
        # Move user from pending to verified
        user_data = pending_users[user_email]['user_data']
        user_data['verified'] = True
        user_data['created_at'] = datetime.now().isoformat()
        
        users = load_users()
        users.append(user_data)
        
        if save_users(users):
            # Remove from pending
            del pending_users[user_email]
            save_pending_users(pending_users)
            return jsonify({'success': True, 'message': 'Акаунтът е потвърден успешно!'})
        else:
            return jsonify({'success': False, 'message': 'Грешка при запазване на потребителя'})
            
    except Exception as e:
        print(f"Verification error: {e}")
        return jsonify({'success': False, 'message': 'Възникна грешка при верификацията'})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email и парола са задължителни'})
        
        users = load_users()
        for user in users:
            if user['email'] == email and user['password'] == password:
                if user.get('verified', False):
                    return jsonify({'success': True, 'message': 'Успешен вход!'})
                else:
                    return jsonify({'success': False, 'message': 'Акаунтът не е потвърден'})
        
        return jsonify({'success': False, 'message': 'Невалиден email или парола'})
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': 'Възникна грешка при влизането'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
