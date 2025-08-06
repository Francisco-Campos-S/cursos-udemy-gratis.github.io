#!/usr/bin/env python3
"""
Script completo para ejecutar todo el proceso de extracción y publicación
"""
import os
import sys
import subprocess
from datetime import datetime

def print_header():
    """Imprimir encabezado del proceso"""
    print("🎓 BOT DE CURSOS UDEMY - PROCESO COMPLETO")
    print("=" * 60)
    print("Este script ejecutará todo el proceso:")
    print("1. Extraer cursos con capturas de pantalla")
    print("2. Crear página web para GitHub Pages")
    print("3. Configurar automatización")
    print("4. Publicar en GitHub")
    print("=" * 60)
    print(f"📅 Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

def check_requirements():
    """Verificar requisitos del sistema"""
    print("🔍 Verificando requisitos del sistema...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Verificar dependencias
    try:
        import selenium
        print("✅ Selenium instalado")
    except ImportError:
        print("❌ Selenium no está instalado")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    # Verificar Chrome
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        print("✅ Chrome disponible")
    except Exception as e:
        print(f"❌ Error con Chrome: {e}")
        print("💡 Asegúrate de tener Google Chrome instalado")
        return False
    
    # Verificar Git
    try:
        result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git disponible")
        else:
            print("❌ Git no está disponible")
            return False
    except:
        print("❌ Git no está disponible")
        return False
    
    print("✅ Todos los requisitos cumplidos")
    return True

def run_extraction():
    """Ejecutar extracción de cursos"""
    print("\n📊 PASO 1: Extrayendo cursos con capturas de pantalla...")
    
    try:
        result = subprocess.run([sys.executable, "extract_and_publish.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Extracción completada exitosamente")
            if result.stdout:
                print("📄 Salida:")
                print(result.stdout)
            return True
        else:
            print("❌ Error en la extracción")
            if result.stderr:
                print("💥 Error:")
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando extracción: {e}")
        return False

def run_publication():
    """Ejecutar publicación en GitHub"""
    print("\n🚀 PASO 2: Publicando en GitHub Pages...")
    
    try:
        result = subprocess.run([sys.executable, "github_publisher.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Publicación completada exitosamente")
            if result.stdout:
                print("📄 Salida:")
                print(result.stdout)
            return True
        else:
            print("❌ Error en la publicación")
            if result.stderr:
                print("💥 Error:")
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando publicación: {e}")
        return False

def show_results():
    """Mostrar resultados del proceso"""
    print("\n📋 RESULTADOS DEL PROCESO")
    print("=" * 40)
    
    # Verificar archivos creados
    files_to_check = [
        ("docs/index.html", "Página web principal"),
        ("docs/courses.json", "Datos de cursos"),
        ("docs/README.md", "Documentación"),
        (".github/workflows/deploy.yml", "Workflow de despliegue"),
        (".github/workflows/auto-extract.yml", "Workflow de automatización")
    ]
    
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (no encontrado)")
    
    # Verificar screenshots
    screenshots_dir = "screenshots"
    if os.path.exists(screenshots_dir):
        screenshot_count = len([f for f in os.listdir(screenshots_dir) if f.endswith('.png')])
        print(f"📸 Capturas de pantalla: {screenshot_count} archivos")
    else:
        print("📸 Capturas de pantalla: No encontradas")
    
    # Verificar repositorio Git
    if os.path.exists(".git"):
        try:
            result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                remote_url = result.stdout.strip()
                print(f"🔗 Repositorio remoto: {remote_url}")
                
                # Extraer información del repositorio
                if "github.com" in remote_url:
                    parts = remote_url.split("github.com/")[1].split(".git")[0]
                    username, repo = parts.split("/")
                    pages_url = f"https://{username}.github.io/{repo}/"
                    print(f"🌐 GitHub Pages URL: {pages_url}")
            else:
                print("🔗 Repositorio remoto: No configurado")
        except:
            print("🔗 Repositorio remoto: Error al verificar")
    else:
        print("🔗 Repositorio Git: No inicializado")

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n📋 PRÓXIMOS PASOS")
    print("=" * 40)
    print("1. 🌐 Ve a tu repositorio en GitHub")
    print("2. ⚙️  Ve a Settings > Pages")
    print("3. 🔧 Selecciona 'GitHub Actions' como fuente")
    print("4. 💾 Guarda los cambios")
    print("5. ⏳ Espera a que se publique la página")
    print("6. 🔄 El bot se ejecutará automáticamente cada día")
    print()
    print("📝 Notas importantes:")
    print("- Los cupones tienen tiempo limitado de validez")
    print("- La página se actualiza automáticamente")
    print("- Puedes ejecutar manualmente desde Actions")
    print("- Revisa los logs si hay problemas")

def main():
    """Función principal"""
    print_header()
    
    # Verificar requisitos
    if not check_requirements():
        print("\n❌ No se pueden cumplir los requisitos")
        print("💡 Instala las dependencias y verifica Chrome")
        return False
    
    # Ejecutar extracción
    if not run_extraction():
        print("\n❌ Error en la extracción")
        return False
    
    # Ejecutar publicación
    if not run_publication():
        print("\n❌ Error en la publicación")
        return False
    
    # Mostrar resultados
    show_results()
    
    # Mostrar próximos pasos
    show_next_steps()
    
    print(f"\n🎉 ¡PROCESO COMPLETADO!")
    print(f"📅 Finalizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Todo el proceso se completó exitosamente")
        else:
            print("\n💥 El proceso falló")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1) 