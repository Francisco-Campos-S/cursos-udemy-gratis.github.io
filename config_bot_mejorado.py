#!/usr/bin/env python3
"""
Configuración para el bot mejorado de 10 cursos
"""

# Configuración del bot
BOT_CONFIG = {
    "max_cursos": 10,                    # Número exacto de cursos a buscar
    "timeout": 10,                       # Timeout para esperar elementos (segundos)
    "delay_between_requests": 2,         # Delay entre requests (segundos)
    "max_retries": 3,                    # Máximo número de reintentos
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Configuración de capturas de pantalla
SCREENSHOT_CONFIG = {
    "max_width": 400,                    # Ancho máximo de las capturas (px)
    "quality": 85,                       # Calidad de compresión (1-100)
    "format": "PNG",                     # Formato de imagen
    "focus_elements": [                  # Elementos en los que enfocar las capturas
        "100% gratis",
        "100% free", 
        "Inscribirse gratis",
        "Get for free",
        "$0",
        "0€",
        "Gratis",
        "Free"
    ]
}

# Configuración de CursosDev
CURSOSDEV_CONFIG = {
    "base_url": "https://cursosdev.com",
    "search_url": "https://cursosdev.com/cupones-udemy/",
    "link_patterns": [                   # Patrones para encontrar enlaces de cursos
        r'https://cursosdev\.com/.*?udemy.*?',
        r'https://www\.udemy\.com/course/.*?',
        r'https://udemy\.com/course/.*?'
    ]
}

# Configuración de Udemy
UDEMY_CONFIG = {
    "base_url": "https://www.udemy.com",
    "price_selectors": [                 # Selectores para encontrar precios
        "span[data-purpose='price-text']",
        ".price-text",
        ".course-price",
        "[data-testid='price-text']"
    ],
    "free_indicators": [                 # Indicadores de que un curso es gratis
        "100% gratis",
        "100% free",
        "Inscribirse gratis",
        "Get for free",
        "Enroll for free"
    ]
}

# Configuración de GitHub Pages
GITHUB_CONFIG = {
    "docs_folder": "docs",               # Carpeta para GitHub Pages
    "html_filename": "index.html",       # Nombre del archivo HTML
    "commit_message": "Actualización automática de cursos gratuitos",
    "branch": "main"                     # Rama principal
}

# Configuración del navegador Chrome
CHROME_CONFIG = {
    "headless": True,                    # Ejecutar en modo headless
    "window_size": "1920x1080",          # Tamaño de ventana
    "disable_images": False,             # Deshabilitar carga de imágenes
    "disable_javascript": False,         # Deshabilitar JavaScript
    "user_data_dir": None,               # Directorio de datos de usuario
    "arguments": [                       # Argumentos adicionales de Chrome
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--disable-extensions",
        "--disable-plugins",
        "--disable-images",
        "--disable-javascript",
        "--disable-css",
        "--disable-fonts",
        "--disable-animations",
        "--disable-video",
        "--disable-audio",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        "--disable-features=TranslateUI",
        "--disable-ipc-flooding-protection"
    ]
}

# Configuración de la página web
WEB_CONFIG = {
    "title": "🎓 Cursos Gratuitos de Udemy",
    "description": "Descubre los mejores cursos gratuitos de Udemy actualizados diariamente",
    "theme": {
        "primary_color": "#667eea",
        "secondary_color": "#764ba2",
        "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "card_background": "rgba(255, 255, 255, 0.95)",
        "text_color": "#333333",
        "link_color": "#667eea"
    },
    "features": {
        "show_timestamp": True,          # Mostrar fecha de actualización
        "show_course_count": True,       # Mostrar número de cursos
        "show_coupon_codes": True,       # Mostrar códigos de cupón
        "show_direct_links": True,       # Mostrar enlaces directos
        "show_screenshots": True,        # Mostrar capturas de pantalla
        "responsive_design": True,       # Diseño responsive
        "dark_mode": False,              # Modo oscuro
        "animations": True               # Animaciones CSS
    }
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",                     # Nivel de logging
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file": "bot_mejorado.log",          # Archivo de log
    "console": True,                     # Mostrar en consola
    "file_output": True                  # Guardar en archivo
}

# Configuración de validación
VALIDATION_CONFIG = {
    "min_course_title_length": 10,       # Longitud mínima del título
    "max_course_title_length": 200,      # Longitud máxima del título
    "required_fields": [                 # Campos requeridos para cada curso
        "title",
        "url",
        "coupon_code",
        "screenshot_path"
    ],
    "price_validation": {                # Validación de precios
        "free_indicators": ["$0", "0€", "Gratis", "Free", "0.00"],
        "max_price": 0.01                # Precio máximo para considerar gratis
    }
}

# Configuración de errores y reintentos
ERROR_CONFIG = {
    "max_network_retries": 3,            # Máximo reintentos de red
    "network_timeout": 30,               # Timeout de red (segundos)
    "element_wait_timeout": 10,          # Timeout para esperar elementos
    "page_load_timeout": 30,             # Timeout de carga de página
    "screenshot_timeout": 5,             # Timeout para capturas
    "retry_delay": 2,                    # Delay entre reintentos (segundos)
    "exponential_backoff": True,         # Backoff exponencial
    "max_backoff_time": 60               # Tiempo máximo de backoff (segundos)
}

# Configuración de optimización
OPTIMIZATION_CONFIG = {
    "compress_images": True,             # Comprimir imágenes
    "resize_images": True,               # Redimensionar imágenes
    "optimize_html": True,               # Optimizar HTML
    "minify_css": True,                  # Minificar CSS
    "cache_control": True,               # Control de caché
    "gzip_compression": True,            # Compresión GZIP
    "lazy_loading": True                 # Carga diferida de imágenes
}

# Configuración de seguridad
SECURITY_CONFIG = {
    "verify_ssl": True,                  # Verificar certificados SSL
    "allow_redirects": True,             # Permitir redirecciones
    "max_redirects": 5,                  # Máximo número de redirecciones
    "timeout": 30,                       # Timeout general (segundos)
    "user_agent_rotation": False,        # Rotación de User-Agent
    "proxy_usage": False,                # Uso de proxy
    "rate_limiting": True,               # Limitación de velocidad
    "requests_per_minute": 30            # Requests por minuto
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    "enable_notifications": False,       # Habilitar notificaciones
    "email_notifications": False,        # Notificaciones por email
    "discord_webhook": None,             # Webhook de Discord
    "telegram_bot": None,                # Bot de Telegram
    "success_notification": True,        # Notificar éxito
    "error_notification": True,          # Notificar errores
    "summary_notification": True         # Notificar resumen
}

# Configuración de estadísticas
STATS_CONFIG = {
    "track_performance": True,           # Rastrear rendimiento
    "save_statistics": True,             # Guardar estadísticas
    "stats_file": "bot_stats.json",      # Archivo de estadísticas
    "track_metrics": [                   # Métricas a rastrear
        "courses_found",
        "courses_processed",
        "screenshots_taken",
        "processing_time",
        "success_rate",
        "error_count"
    ]
}

# Configuración de backup
BACKUP_CONFIG = {
    "enable_backup": True,               # Habilitar backup
    "backup_folder": "backups",          # Carpeta de backup
    "backup_frequency": "daily",         # Frecuencia de backup
    "max_backups": 7,                    # Máximo número de backups
    "backup_files": [                    # Archivos a hacer backup
        "courses.json",
        "bot_mejorado.log",
        "bot_stats.json"
    ]
}

# Configuración de limpieza
CLEANUP_CONFIG = {
    "enable_cleanup": True,              # Habilitar limpieza
    "cleanup_old_screenshots": True,     # Limpiar capturas antiguas
    "cleanup_old_logs": True,            # Limpiar logs antiguos
    "cleanup_old_backups": True,         # Limpiar backups antiguos
    "max_screenshot_age": 7,             # Edad máxima de capturas (días)
    "max_log_age": 30,                   # Edad máxima de logs (días)
    "max_backup_age": 90                 # Edad máxima de backups (días)
}

# Configuración de desarrollo
DEV_CONFIG = {
    "debug_mode": False,                 # Modo debug
    "verbose_output": False,             # Salida verbosa
    "save_debug_info": False,            # Guardar información de debug
    "test_mode": False,                  # Modo de prueba
    "dry_run": False,                    # Ejecución sin cambios
    "profile_performance": False,        # Perfil de rendimiento
    "memory_tracking": False             # Rastreo de memoria
}

# Exportar todas las configuraciones
ALL_CONFIGS = {
    "bot": BOT_CONFIG,
    "screenshot": SCREENSHOT_CONFIG,
    "cursosdev": CURSOSDEV_CONFIG,
    "udemy": UDEMY_CONFIG,
    "github": GITHUB_CONFIG,
    "chrome": CHROME_CONFIG,
    "web": WEB_CONFIG,
    "logging": LOGGING_CONFIG,
    "validation": VALIDATION_CONFIG,
    "error": ERROR_CONFIG,
    "optimization": OPTIMIZATION_CONFIG,
    "security": SECURITY_CONFIG,
    "notification": NOTIFICATION_CONFIG,
    "stats": STATS_CONFIG,
    "backup": BACKUP_CONFIG,
    "cleanup": CLEANUP_CONFIG,
    "dev": DEV_CONFIG
}

def get_config(section):
    """Obtener configuración de una sección específica"""
    return ALL_CONFIGS.get(section, {})

def update_config(section, key, value):
    """Actualizar una configuración específica"""
    if section in ALL_CONFIGS and key in ALL_CONFIGS[section]:
        ALL_CONFIGS[section][key] = value
        return True
    return False

def reset_config():
    """Resetear todas las configuraciones a valores por defecto"""
    # Esta función recargaría las configuraciones originales
    pass

if __name__ == "__main__":
    # Mostrar configuración actual
    print("🔧 Configuración del Bot Mejorado")
    print("=" * 50)
    
    for section, config in ALL_CONFIGS.items():
        print(f"\n📋 {section.upper()}:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    print(f"\n✅ Total de secciones de configuración: {len(ALL_CONFIGS)}") 