#!/usr/bin/env python3
"""
Script para crear un nuevo repositorio público para GitHub Pages
con los cursos extraídos
"""
import os
import subprocess
import json
from datetime import datetime

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

def create_new_repository_structure():
    """Crear estructura para nuevo repositorio de GitHub Pages"""
    print("📁 Creando estructura para nuevo repositorio...")
    
    # Crear directorio para el nuevo repositorio
    new_repo_dir = "cursos-udemy-gratis"
    if os.path.exists(new_repo_dir):
        print(f"⚠️ El directorio {new_repo_dir} ya existe")
        return new_repo_dir
    
    os.makedirs(new_repo_dir)
    
    # Copiar archivos necesarios
    files_to_copy = [
        ("docs/index.html", "index.html"),
        ("docs/courses.json", "courses.json"),
        ("docs/README.md", "README.md")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            import shutil
            shutil.copy2(src, os.path.join(new_repo_dir, dst))
            print(f"✅ Copiado: {src} -> {new_repo_dir}/{dst}")
    
    # Copiar screenshots
    screenshots_dir = os.path.join(new_repo_dir, "screenshots")
    if os.path.exists("screenshots"):
        import shutil
        shutil.copytree("screenshots", screenshots_dir)
        print(f"✅ Copiado directorio: screenshots -> {new_repo_dir}/screenshots")
    
    # Crear .gitignore
    gitignore_content = """# Archivos del sistema
.DS_Store
Thumbs.db

# Archivos de Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Archivos de IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Archivos temporales
*.tmp
*.temp

# Archivos de configuración local
.env
config.local.py

# Archivos de Chrome
chromedriver.exe
chromedriver
"""
    
    with open(os.path.join(new_repo_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    # Crear README principal
    readme_content = """# 🎓 Cursos Gratuitos de Udemy

Página web con cursos gratuitos de Udemy extraídos de CursosDev.

## 🌐 Página Web

**Visita la página web:** [https://TU_USUARIO.github.io/cursos-udemy-gratis/](https://TU_USUARIO.github.io/cursos-udemy-gratis/)

## 📊 Características

- ✅ **Cursos gratuitos** de Udemy con cupones
- 📸 **Capturas de pantalla** de cada curso
- 🎫 **Códigos de cupón** incluidos
- 🌐 **Página web moderna** y responsive
- 🤖 **Actualización automática** diaria
- 📱 **Solo web** - Sin WhatsApp

## 🚀 Cómo usar

1. **Visita la página web** en el enlace de arriba
2. **Explora los cursos** disponibles
3. **Haz clic en "Obtener Curso Gratis"** para ir al curso
4. **Usa el código de cupón** para obtener el descuento

## 📋 Requisitos

- Navegador web moderno
- Conexión a internet
- Cuenta de Udemy (gratuita)

## 🔄 Actualización

Los cursos se actualizan automáticamente cada día a las 8:00 AM UTC.

## 📝 Notas

- Los cupones tienen tiempo limitado de validez
- Los cursos son extraídos de CursosDev
- Esta página es solo informativa
- No se envían mensajes a WhatsApp

## 🤝 Contribuir

Si encuentras un curso que no funciona o quieres sugerir mejoras:

1. Ve a [Issues](https://github.com/TU_USUARIO/cursos-udemy-gratis/issues)
2. Crea un nuevo issue
3. Describe el problema o sugerencia

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¡Disfruta de los cursos gratuitos! 🎓**

**📱 Recuerda: Solo página web, sin WhatsApp**
"""
    
    with open(os.path.join(new_repo_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Crear workflow de GitHub Pages
    workflows_dir = os.path.join(new_repo_dir, ".github", "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    
    workflow_content = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: '.'
        
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
"""
    
    with open(os.path.join(workflows_dir, "deploy.yml"), "w") as f:
        f.write(workflow_content)
    
    print(f"✅ Estructura creada en: {new_repo_dir}")
    return new_repo_dir

def setup_git_repository(repo_dir):
    """Configurar repositorio Git"""
    print(f"🔧 Configurando Git en {repo_dir}...")
    
    # Cambiar al directorio del repositorio
    os.chdir(repo_dir)
    
    # Inicializar Git
    if not run_command("git init", "Inicializando Git"):
        return False
    
    # Agregar archivos
    if not run_command("git add .", "Agregando archivos"):
        return False
    
    # Hacer commit inicial
    if not run_command('git commit -m "Initial commit - Cursos Udemy Gratis"', "Haciendo commit inicial"):
        return False
    
    print("✅ Repositorio Git configurado")
    return True

def create_github_repository_instructions():
    """Mostrar instrucciones para crear el repositorio en GitHub"""
    print("\n📋 INSTRUCCIONES PARA CREAR EL REPOSITORIO EN GITHUB")
    print("=" * 60)
    print("1. Ve a https://github.com/new")
    print("2. Nombre del repositorio: cursos-udemy-gratis")
    print("3. Descripción: Cursos gratuitos de Udemy con cupones")
    print("4. Marca como PÚBLICO")
    print("5. NO inicialices con README (ya lo tenemos)")
    print("6. Haz clic en 'Create repository'")
    print()
    print("7. Después de crear el repositorio, ejecuta estos comandos:")
    print("   cd cursos-udemy-gratis")
    print("   git remote add origin https://github.com/TU_USUARIO/cursos-udemy-gratis.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("8. Ve a Settings > Pages")
    print("9. Selecciona 'GitHub Actions' como fuente")
    print("10. La página estará disponible en:")
    print("    https://TU_USUARIO.github.io/cursos-udemy-gratis/")

def main():
    """Función principal"""
    print("🚀 CREADOR DE REPOSITORIO PARA GITHUB PAGES")
    print("=" * 50)
    print("Este script creará un nuevo repositorio público")
    print("específicamente para la página de GitHub Pages")
    print("=" * 50)
    
    # Crear estructura del repositorio
    repo_dir = create_new_repository_structure()
    if not repo_dir:
        print("❌ Error creando estructura del repositorio")
        return
    
    # Configurar Git
    if not setup_git_repository(repo_dir):
        print("❌ Error configurando Git")
        return
    
    # Mostrar instrucciones
    create_github_repository_instructions()
    
    print(f"\n🎉 ¡Repositorio preparado en: {repo_dir}")
    print("📁 Archivos creados:")
    print("   - index.html (página principal)")
    print("   - courses.json (datos de cursos)")
    print("   - README.md (documentación)")
    print("   - screenshots/ (capturas de pantalla)")
    print("   - .github/workflows/deploy.yml (workflow)")
    print("   - .gitignore (archivos a ignorar)")
    
    print(f"\n📋 Próximos pasos:")
    print("1. Crea el repositorio en GitHub (ver instrucciones arriba)")
    print("2. Ejecuta los comandos Git mostrados")
    print("3. Configura GitHub Pages")
    print("4. ¡Tu página estará lista!")

if __name__ == "__main__":
    main() 