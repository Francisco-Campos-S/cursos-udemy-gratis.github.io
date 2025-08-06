import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Facebook Configuration
    FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL')
    FACEBOOK_PASSWORD = os.getenv('FACEBOOK_PASSWORD')
    FACEBOOK_GROUP_URLS = [
        os.getenv('FACEBOOK_GROUP_URL_1'),
        os.getenv('FACEBOOK_GROUP_URL_2')
    ]
    
    # WhatsApp Configuration
    WHATSAPP_PHONE_NUMBER = os.getenv('WHATSAPP_PHONE_NUMBER')  # Formato: +34612345678
    WHATSAPP_MESSAGE_DELAY = 30  # Segundos entre mensajes
    
    # Scraping Configuration
    SCROLL_PAUSE_TIME = 3  # Segundos para esperar después de hacer scroll
    MAX_POSTS_TO_CHECK = 50  # Máximo número de posts a revisar
    SCREENSHOT_DELAY = 2  # Segundos para esperar antes de tomar screenshot
    
    # Keywords para identificar cursos gratuitos
    FREE_KEYWORDS = [
        'gratis', 'gratuito', 'free', 'sin costo', '0€', '$0', 'gratuito',
        'completamente gratis', '100% gratis', 'totalmente gratis'
    ]
    
    # URLs de plataformas de cursos
    COURSE_PLATFORMS = [
        'udemy.com',
        'coursera.org',
        'edx.org',
        'platzi.com',
        'domestika.org'
    ]
    
    # Directorios
    SCREENSHOTS_DIR = 'screenshots'
    LOGS_DIR = 'logs'
    
    # Configuración del navegador
    BROWSER_HEADLESS = False  # Cambiar a True para ejecutar sin interfaz gráfica
    BROWSER_TIMEOUT = 30 