#!/usr/bin/env python3
"""
Script simple para ejecutar el bot mejorado simplificado
"""

import os
import sys
import subprocess

def check_dependencies():
    """Verificar dependencias básicas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = ['selenium', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} instalado")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} no instalado")
    
    if missing_packages:
        print(f"\n⚠️ Faltan dependencias: {', '.join(missing_packages)}")
        print("💡 Instala las dependencias con:")
        print("pip install selenium Pillow")
        return False
    
    return True

def check_chrome():
    """Verificar que Chrome esté disponible"""
    print("\n🌐 Verificando Chrome...")
    
    # Verificar si Chrome está instalado en Windows
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome encontrado en: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("⚠️ Chrome no encontrado en las ubicaciones típicas")
        print("💡 Asegúrate de tener Chrome instalado")
        print("💡 Descarga desde: https://www.google.com/chrome/")
        return False
    
    return True

def check_chromedriver():
    """Verificar ChromeDriver"""
    print("\n🔧 Verificando ChromeDriver...")
    
    try:
        # Intentar importar y usar ChromeDriver
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Intentar crear driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        
        print("✅ ChromeDriver funciona correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error con ChromeDriver: {str(e)}")
        print("💡 Descarga ChromeDriver desde: https://chromedriver.chromium.org/")
        print("💡 Asegúrate de que esté en el PATH o en el directorio del proyecto")
        return False

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

def run_bot():
    """Ejecutar el bot"""
    print("\n🚀 Ejecutando bot mejorado...")
    print("=" * 50)
    
    try:
        # Importar y ejecutar el bot
        from bot_mejorado_simple import main
        main()
        
    except ImportError as e:
        print(f"❌ Error al importar el bot: {str(e)}")
        print("💡 Verifica que el archivo bot_mejorado_simple.py esté presente")
    except Exception as e:
        print(f"❌ Error al ejecutar el bot: {str(e)}")

def show_help():
    """Mostrar ayuda"""
    print("""
🤖 SCRIPT DE EJECUCIÓN DEL BOT MEJORADO

Uso:
  python ejecutar_bot_simple.py [opción]

Opciones:
  --help, -h          Mostrar esta ayuda
  --check, -c         Solo verificar dependencias
  --run, -r           Ejecutar bot directamente
  --full, -f          Verificación completa + ejecución (por defecto)

Ejemplos:
  python ejecutar_bot_simple.py          # Verificación completa + ejecución
  python ejecutar_bot_simple.py --check  # Solo verificar dependencias
  python ejecutar_bot_simple.py --run    # Ejecutar bot directamente
  python ejecutar_bot_simple.py --help   # Mostrar ayuda

Requisitos:
  - Python 3.8+
  - Chrome navegador
  - ChromeDriver
  - Git configurado
  - Repositorio con remote origin
""")

def main():
    """Función principal"""
    print("🤖 BOT MEJORADO - EJECUTOR SIMPLE")
    print("=" * 40)
    
    # Procesar argumentos
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h']:
            show_help()
            return
        elif arg in ['--check', '-c']:
            print("🔍 MODO VERIFICACIÓN")
            print("=" * 30)
            
            checks = [
                ("Dependencias", check_dependencies),
                ("Chrome", check_chrome),
                ("ChromeDriver", check_chromedriver),
                ("Git", check_git)
            ]
            
            passed = 0
            total = len(checks)
            
            for check_name, check_func in checks:
                try:
                    if check_func():
                        passed += 1
                    else:
                        print(f"❌ Verificación '{check_name}' falló")
                except Exception as e:
                    print(f"❌ Error en verificación '{check_name}': {str(e)}")
            
            print(f"\n📊 Resultados: {passed}/{total} verificaciones pasaron")
            
            if passed == total:
                print("✅ Todas las verificaciones pasaron")
            else:
                print("⚠️ Algunas verificaciones fallaron")
            
            return
        elif arg in ['--run', '-r']:
            print("🚀 MODO EJECUCIÓN DIRECTA")
            print("=" * 30)
            run_bot()
            return
        elif arg in ['--full', '-f']:
            pass  # Continuar con verificación completa + ejecución
        else:
            print(f"❌ Opción desconocida: {arg}")
            show_help()
            return
    
    # Modo por defecto: verificación completa + ejecución
    print("🔍 VERIFICACIÓN COMPLETA")
    print("=" * 30)
    
    checks = [
        ("Dependencias", check_dependencies),
        ("Chrome", check_chrome),
        ("ChromeDriver", check_chromedriver),
        ("Git", check_git)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                print(f"❌ Verificación '{check_name}' falló")
        except Exception as e:
            print(f"❌ Error en verificación '{check_name}': {str(e)}")
    
    print(f"\n📊 Resultados: {passed}/{total} verificaciones pasaron")
    
    if passed == total:
        print("✅ Todas las verificaciones pasaron")
        print("\n🚀 Iniciando ejecución del bot...")
        run_bot()
    else:
        print("⚠️ Algunas verificaciones fallaron")
        print("💡 Corrige los problemas antes de ejecutar el bot")
        print("💡 Usa --help para más información")

if __name__ == "__main__":
    main() 