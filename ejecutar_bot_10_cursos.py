#!/usr/bin/env python3
"""
Script simple para ejecutar el bot mejorado de 10 cursos
"""
import os
import sys

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'selenium',
        'PIL',
        'webdriver_manager'
    ]
    
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
        print("pip install selenium Pillow webdriver-manager")
        return False
    
    return True

def check_git_repo():
    """Verificar que sea un repositorio Git"""
    print("🔍 Verificando repositorio Git...")
    
    if not os.path.exists(".git"):
        print("❌ No es un repositorio Git")
        print("💡 Ejecuta estos comandos:")
        print("   git init")
        print("   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git")
        return False
    
    print("✅ Repositorio Git encontrado")
    return True

def main():
    """Función principal"""
    print("🚀 Ejecutor del Bot Mejorado - 10 Cursos")
    print("=" * 50)
    print("🎯 Busca exactamente 10 cursos gratuitos")
    print("📸 Toma capturas enfocadas y pequeñas")
    print("🌐 Publica en GitHub Pages")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        return False
    
    # Verificar repositorio Git
    if not check_git_repo():
        return False
    
    # Ejecutar el bot
    print("\n🚀 Ejecutando bot mejorado...")
    try:
        from bot_mejorado_10_cursos import main as run_bot
        success = run_bot()
        
        if success:
            print("\n🎉 ¡Bot ejecutado exitosamente!")
            print("📋 Próximos pasos:")
            print("1. Ve a tu repositorio en GitHub")
            print("2. Ve a Settings > Pages")
            print("3. Selecciona 'GitHub Actions' como fuente")
            print("4. La página se publicará automáticamente")
            print("5. Los cursos estarán disponibles en GitHub Pages")
        else:
            print("\n❌ Error ejecutando el bot")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando el bot: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 