#!/usr/bin/env python3
"""
Script para automatizar la publicación en GitHub Pages
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

def check_git_status():
    """Verificar estado de Git"""
    print("🔍 Verificando estado de Git...")
    
    # Verificar si es un repositorio Git
    if not os.path.exists(".git"):
        print("❌ No es un repositorio Git")
        print("💡 Ejecuta 'git init' para inicializar el repositorio")
        return False
    
    # Verificar estado
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Hay cambios pendientes:")
        print(result.stdout.strip())
        return True
    else:
        print("✅ No hay cambios pendientes")
        return False

def commit_and_push_changes():
    """Hacer commit y push de los cambios"""
    print("📤 Subiendo cambios a GitHub...")
    
    # Agregar todos los archivos
    if not run_command("git add .", "Agregando archivos"):
        return False
    
    # Hacer commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Actualizar cursos - {timestamp}"
    if not run_command(f'git commit -m "{commit_message}"', "Haciendo commit"):
        return False
    
    # Hacer push
    if not run_command("git push origin main", "Subiendo a GitHub"):
        return False
    
    return True

def setup_github_pages():
    """Configurar GitHub Pages"""
    print("🌐 Configurando GitHub Pages...")
    
    # Verificar si existe el archivo de configuración de GitHub Pages
    if os.path.exists(".github/workflows/deploy.yml"):
        print("✅ Workflow de GitHub Pages ya configurado")
        return True
    
    # Crear directorio .github/workflows
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Crear workflow de GitHub Pages
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
        path: './docs'
        
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
    
    with open(".github/workflows/deploy.yml", "w") as f:
        f.write(workflow_content)
    
    print("✅ Workflow de GitHub Pages creado")
    return True

def create_github_workflow():
    """Crear workflow para automatizar la extracción"""
    print("🤖 Creando workflow de automatización...")
    
    # Crear directorio .github/workflows si no existe
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Crear workflow de automatización
    workflow_content = """name: Extract and Deploy Courses

on:
  schedule:
    # Ejecutar cada día a las 8:00 AM UTC
    - cron: '0 8 * * *'
  workflow_dispatch:  # Permitir ejecución manual

jobs:
  extract-courses:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install Chrome
      run: |
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install selenium webdriver-manager
        
    - name: Extract courses
      run: |
        python extract_and_publish.py
        
    - name: Commit and push changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --quiet && git diff --staged --quiet || git commit -m "Auto-update courses $(date)"
        git push
        
  deploy:
    needs: extract-courses
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
      
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: './docs'
        
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
"""
    
    with open(".github/workflows/auto-extract.yml", "w") as f:
        f.write(workflow_content)
    
    print("✅ Workflow de automatización creado")
    return True

def get_repository_info():
    """Obtener información del repositorio"""
    try:
        result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            # Extraer usuario y repositorio de la URL
            if "github.com" in remote_url:
                parts = remote_url.split("github.com/")[1].split(".git")[0]
                username, repo = parts.split("/")
                return username, repo
    except:
        pass
    return None, None

def main():
    """Función principal"""
    print("🚀 Publicador de GitHub Pages")
    print("=" * 40)
    
    # Verificar si es un repositorio Git
    if not os.path.exists(".git"):
        print("❌ No es un repositorio Git")
        print("💡 Ejecuta estos comandos:")
        print("   git init")
        print("   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git")
        return
    
    # Obtener información del repositorio
    username, repo = get_repository_info()
    if username and repo:
        print(f"📦 Repositorio: {username}/{repo}")
        print(f"🌐 URL de GitHub Pages: https://{username}.github.io/{repo}/")
    else:
        print("⚠️ No se pudo obtener información del repositorio")
    
    # Verificar estado
    if not check_git_status():
        print("💡 No hay cambios para subir")
        return
    
    # Configurar GitHub Pages
    if not setup_github_pages():
        print("❌ Error configurando GitHub Pages")
        return
    
    # Crear workflow de automatización
    if not create_github_workflow():
        print("❌ Error creando workflow")
        return
    
    # Subir cambios
    if not commit_and_push_changes():
        print("❌ Error subiendo cambios")
        return
    
    print("\n🎉 ¡Publicación completada!")
    print("📋 Próximos pasos:")
    print("1. Ve a Settings > Pages en tu repositorio")
    print("2. Selecciona 'GitHub Actions' como fuente")
    print("3. La página se publicará automáticamente")
    print("4. El workflow se ejecutará diariamente para actualizar los cursos")
    
    if username and repo:
        print(f"\n🔗 Tu página estará disponible en:")
        print(f"   https://{username}.github.io/{repo}/")

if __name__ == "__main__":
    main() 