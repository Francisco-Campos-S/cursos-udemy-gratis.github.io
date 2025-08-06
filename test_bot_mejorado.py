#!/usr/bin/env python3
"""
Script de prueba para el bot mejorado
Verifica que todas las dependencias y configuraciones estén correctas
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} no es compatible")
        print("💡 Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = {
        'selenium': 'Selenium WebDriver',
        'PIL': 'Pillow (PIL)',
        'webdriver_manager': 'WebDriver Manager'
    }
    
    missing_packages = []
    installed_packages = []
    
    for package, description in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {description} - Instalado")
            installed_packages.append(package)
        except ImportError:
            print(f"❌ {description} - No instalado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Faltan dependencias: {', '.join(missing_packages)}")
        print("💡 Instala las dependencias con:")
        print("pip install selenium Pillow webdriver-manager")
        return False
    
    print(f"\n✅ Todas las dependencias están instaladas ({len(installed_packages)}/{len(required_packages)})")
    return True

def check_chrome():
    """Verificar que Chrome esté disponible"""
    print("\n🌐 Verificando Chrome...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Intentar inicializar el driver
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver encontrado en: {driver_path}")
        
        # Crear driver de prueba
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        
        print("✅ Chrome está funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con Chrome: {str(e)}")
        print("💡 Asegúrate de tener Chrome instalado")
        return False

def check_files():
    """Verificar archivos necesarios"""
    print("\n📁 Verificando archivos...")
    
    required_files = [
        'bot_mejorado_10_cursos.py',
        'config_bot_mejorado.py',
        'ejecutar_bot_10_cursos.py'
    ]
    
    missing_files = []
    existing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Existe")
            existing_files.append(file)
        else:
            print(f"❌ {file} - No existe")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Faltan archivos: {', '.join(missing_files)}")
        return False
    
    print(f"\n✅ Todos los archivos están presentes ({len(existing_files)}/{len(required_files)})")
    return True

def check_git():
    """Verificar configuración de Git"""
    print("\n🔧 Verificando Git...")
    
    try:
        # Verificar si es un repositorio Git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Repositorio Git configurado")
            
            # Verificar remote origin
            remote_result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'origin' in remote_result.stdout:
                print("✅ Remote origin configurado")
                return True
            else:
                print("⚠️ Remote origin no configurado")
                print("💡 Configura con: git remote add origin <URL>")
                return False
        else:
            print("❌ No es un repositorio Git")
            print("💡 Inicializa con: git init")
            return False
            
    except FileNotFoundError:
        print("❌ Git no está instalado")
        print("💡 Instala Git desde: https://git-scm.com/")
        return False

def check_config():
    """Verificar configuración del bot"""
    print("\n⚙️ Verificando configuración...")
    
    try:
        from config_bot_mejorado import ALL_CONFIGS, get_config
        
        # Verificar secciones principales
        required_sections = ['bot', 'screenshot', 'cursosdev', 'udemy', 'github']
        
        for section in required_sections:
            config = get_config(section)
            if config:
                print(f"✅ Configuración {section} - OK")
            else:
                print(f"❌ Configuración {section} - Faltante")
                return False
        
        # Verificar configuración específica
        bot_config = get_config('bot')
        if bot_config.get('max_cursos') == 10:
            print("✅ Configuración de 10 cursos - OK")
        else:
            print("❌ Configuración de 10 cursos - Incorrecta")
            return False
        
        screenshot_config = get_config('screenshot')
        if screenshot_config.get('max_width') == 400:
            print("✅ Configuración de capturas pequeñas - OK")
        else:
            print("❌ Configuración de capturas pequeñas - Incorrecta")
            return False
        
        print("✅ Todas las configuraciones están correctas")
        return True
        
    except ImportError as e:
        print(f"❌ Error al importar configuración: {str(e)}")
        return False

def test_web_creation():
    """Probar creación de página web"""
    print("\n🌐 Probando creación de página web...")
    
    try:
        # Importar función de creación de HTML
        from bot_mejorado_10_cursos import create_html_page
        
        # Datos de prueba
        test_courses = [
            {
                'title': 'Curso de Prueba 1',
                'url': 'https://www.udemy.com/course/test1/',
                'coupon_code': 'TEST1FREE',
                'screenshot_path': 'test_screenshot1.png'
            },
            {
                'title': 'Curso de Prueba 2',
                'url': 'https://www.udemy.com/course/test2/',
                'coupon_code': 'TEST2FREE',
                'screenshot_path': 'test_screenshot2.png'
            }
        ]
        
        # Crear directorio docs si no existe
        docs_dir = Path('docs')
        docs_dir.mkdir(exist_ok=True)
        
        # Crear página de prueba
        html_content = create_html_page(test_courses)
        
        # Guardar archivo de prueba
        test_file = docs_dir / 'test.html'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ Página web de prueba creada correctamente")
        
        # Limpiar archivo de prueba
        test_file.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear página web: {str(e)}")
        return False

def run_full_test():
    """Ejecutar todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DEL BOT MEJORADO")
    print("=" * 50)
    
    tests = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Chrome", check_chrome),
        ("Archivos", check_files),
        ("Git", check_git),
        ("Configuración", check_config),
        ("Creación Web", test_web_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ Prueba '{test_name}' falló")
        except Exception as e:
            print(f"❌ Error en prueba '{test_name}': {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS DE LAS PRUEBAS")
    print(f"✅ Pruebas pasadas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("🚀 El bot está listo para ejecutarse")
        print("\n💡 Para ejecutar el bot:")
        print("   python ejecutar_bot_10_cursos.py")
        return True
    else:
        print(f"\n⚠️ {total - passed} prueba(s) falló(aron)")
        print("🔧 Corrige los problemas antes de ejecutar el bot")
        return False

def show_help():
    """Mostrar ayuda"""
    print("""
🔧 SCRIPT DE PRUEBA DEL BOT MEJORADO

Uso:
  python test_bot_mejorado.py [opción]

Opciones:
  --help, -h          Mostrar esta ayuda
  --quick, -q         Prueba rápida (solo dependencias)
  --full, -f          Prueba completa (por defecto)

Ejemplos:
  python test_bot_mejorado.py          # Prueba completa
  python test_bot_mejorado.py --quick  # Prueba rápida
  python test_bot_mejorado.py --help   # Mostrar ayuda
""")

def quick_test():
    """Prueba rápida"""
    print("⚡ PRUEBA RÁPIDA DEL BOT MEJORADO")
    print("=" * 40)
    
    tests = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Archivos", check_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ Prueba '{test_name}' falló")
        except Exception as e:
            print(f"❌ Error en prueba '{test_name}': {str(e)}")
    
    print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("✅ Prueba rápida exitosa")
        return True
    else:
        print("❌ Prueba rápida falló")
        return False

if __name__ == "__main__":
    # Procesar argumentos de línea de comandos
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h']:
            show_help()
        elif arg in ['--quick', '-q']:
            quick_test()
        elif arg in ['--full', '-f']:
            run_full_test()
        else:
            print(f"❌ Opción desconocida: {arg}")
            show_help()
    else:
        # Ejecutar prueba completa por defecto
        run_full_test() 