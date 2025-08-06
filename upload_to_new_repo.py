#!/usr/bin/env python3
"""
Script para subir el nuevo repositorio de GitHub Pages a GitHub
"""
import os
import subprocess
import getpass

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            if result.stdout:
                print(f"📄 Salida: {result.stdout.strip()}")
        else:
            print(f"❌ Error en {description}")
            if result.stderr:
                print(f"💥 Error: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def get_github_username():
    """Obtener el nombre de usuario de GitHub"""
    print("🔍 Necesito tu nombre de usuario de GitHub")
    username = input("Ingresa tu nombre de usuario de GitHub: ").strip()
    if not username:
        print("❌ Nombre de usuario requerido")
        return None
    return username

def setup_remote_repository(username):
    """Configurar el repositorio remoto"""
    print(f"🔗 Configurando repositorio remoto para {username}...")
    
    # Cambiar al directorio del repositorio
    repo_dir = "cursos-udemy-gratis"
    if not os.path.exists(repo_dir):
        print(f"❌ El directorio {repo_dir} no existe")
        return False
    
    os.chdir(repo_dir)
    
    # Configurar el remote origin
    remote_url = f"https://github.com/{username}/cursos-udemy-gratis.git"
    if not run_command(f'git remote add origin {remote_url}', "Agregando remote origin"):
        return False
    
    # Cambiar a rama main
    if not run_command("git branch -M main", "Cambiando a rama main"):
        return False
    
    return True

def push_to_github():
    """Subir a GitHub"""
    print("📤 Subiendo a GitHub...")
    
    # Hacer push
    if not run_command("git push -u origin main", "Subiendo a GitHub"):
        return False
    
    return True

def show_final_instructions(username):
    """Mostrar instrucciones finales"""
    print("\n🎉 ¡REPOSITORIO SUBIDO EXITOSAMENTE!")
    print("=" * 50)
    print(f"📦 Repositorio: {username}/cursos-udemy-gratis")
    print(f"🌐 URL del repositorio: https://github.com/{username}/cursos-udemy-gratis")
    print(f"🌐 URL de GitHub Pages: https://{username}.github.io/cursos-udemy-gratis/")
    
    print("\n📋 CONFIGURACIÓN FINAL DE GITHUB PAGES:")
    print("1. Ve a https://github.com/{username}/cursos-udemy-gratis")
    print("2. Haz clic en 'Settings' (pestaña)")
    print("3. En el menú lateral, haz clic en 'Pages'")
    print("4. En 'Source', selecciona 'GitHub Actions'")
    print("5. Guarda los cambios")
    print("6. Espera unos minutos a que se publique")
    
    print(f"\n🌐 Tu página estará disponible en:")
    print(f"   https://{username}.github.io/cursos-udemy-gratis/")
    
    print("\n📱 CARACTERÍSTICAS DE LA PÁGINA:")
    print("- ✅ Cursos gratuitos de Udemy")
    print("- 📸 Capturas de pantalla incluidas")
    print("- 🎫 Códigos de cupón destacados")
    print("- 🌐 Diseño moderno y responsive")
    print("- 📱 Solo web - Sin WhatsApp")
    
    print("\n🔄 PRÓXIMAS ACTUALIZACIONES:")
    print("- Los cursos se actualizarán automáticamente")
    print("- Puedes ejecutar manualmente desde Actions")
    print("- La página se actualiza cada día")

def main():
    """Función principal"""
    print("🚀 SUBIDOR DE REPOSITORIO A GITHUB")
    print("=" * 40)
    print("Este script subirá el repositorio de GitHub Pages")
    print("a tu cuenta de GitHub")
    print("=" * 40)
    
    # Obtener nombre de usuario
    username = get_github_username()
    if not username:
        return
    
    print(f"\n📋 RESUMEN:")
    print(f"Usuario: {username}")
    print(f"Repositorio: cursos-udemy-gratis")
    print(f"URL: https://github.com/{username}/cursos-udemy-gratis")
    
    # Confirmar
    confirm = input("\n¿Continuar? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Configurar repositorio remoto
    if not setup_remote_repository(username):
        print("❌ Error configurando repositorio remoto")
        return
    
    # Subir a GitHub
    if not push_to_github():
        print("❌ Error subiendo a GitHub")
        return
    
    # Mostrar instrucciones finales
    show_final_instructions(username)
    
    print(f"\n🎓 ¡Tu página de cursos gratuitos está lista!")
    print("📱 Recuerda: Solo publicación web, sin WhatsApp")

if __name__ == "__main__":
    main() 