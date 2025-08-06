#!/usr/bin/env python3
"""
Script para extraer cursos con capturas de pantalla y publicarlos en GitHub Pages
SIN envío a WhatsApp - Solo publicación web
"""
import os
import time
import re
import json
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_course_id(url):
    """Extraer el ID único del curso de Udemy"""
    try:
        match = re.search(r'/course/([^/?]+)', url)
        if match:
            return match.group(1)
        return url
    except:
        return url

def extract_course_name(url):
    """Extraer el nombre legible del curso de Udemy"""
    try:
        match = re.search(r'/course/([^/?]+)', url)
        if match:
            course_id = match.group(1)
            if course_id.isdigit():
                return f"Curso de Udemy (ID: {course_id})"
            course_name = course_id.replace('-', ' ').replace('_', ' ')
            course_name = ' '.join(word.capitalize() for word in course_name.split())
            return course_name
        return "Curso de Udemy"
    except:
        return "Curso de Udemy"

def extract_coupon_code_from_url(url):
    """Extraer código de cupón de la URL"""
    try:
        discount_match = re.search(r'discountCode=([A-Z0-9]+)', url)
        if discount_match:
            return discount_match.group(1)
        
        coupon_match = re.search(r'couponCode=([A-Z0-9]+)', url)
        if coupon_match:
            return coupon_match.group(1)
        
        return None
    except:
        return None

def take_screenshot(driver, course_name, index):
    """Tomar captura de pantalla del curso"""
    try:
        # Crear directorio de screenshots si no existe
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        # Generar nombre de archivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^\w\s-]', '', course_name).strip()
        safe_name = re.sub(r'[-\s]+', '-', safe_name)
        filename = f"{index:02d}_{safe_name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        # Tomar screenshot
        driver.save_screenshot(filepath)
        print(f"Screenshot guardado: {filepath}")
        
        return filepath
    except Exception as e:
        print(f"Error tomando screenshot: {e}")
        return None

def extract_courses_with_screenshots():
    """Extraer cursos con capturas de pantalla"""
    print("Extrayendo cursos con capturas de pantalla...")
    print("SOLO PUBLICACION WEB - Sin envio a WhatsApp")
    
    driver = None
    courses = []
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navegar a CursosDev
        print("Navegando a CursosDev...")
        driver.get("https://cursosdev.com/")
        time.sleep(3)
        
        # Hacer scroll para cargar más cursos
        print("Cargando cursos...")
        for scroll in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Buscar enlaces de cursos
        course_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'udemy.com') or contains(@href, 'coupons-udemy')]")
        print(f"Encontrados {len(course_links)} enlaces de cursos")
        
        processed_courses = set()
        max_courses = 15  # Limitar a 15 cursos para la web
        
        for i, link in enumerate(course_links[:max_courses]):
            try:
                href = link.get_attribute("href")
                if not href or href in processed_courses:
                    continue
                
                print(f"\nProcesando curso {i+1}/{min(len(course_links), max_courses)}...")
                
                # Navegar al curso
                driver.get(href)
                time.sleep(3)
                
                # Buscar botón de cupón
                coupon_button = None
                for selector in [
                    "//a[contains(text(), 'Obtener Cupón')]",
                    "//button[contains(text(), 'Obtener Cupón')]",
                    "//a[contains(text(), 'cupón')]",
                    "//button[contains(text(), 'cupón')]"
                ]:
                    try:
                        buttons = driver.find_elements(By.XPATH, selector)
                        if buttons:
                            coupon_button = buttons[0]
                            break
                    except:
                        continue
                
                if coupon_button:
                    # Obtener href del botón
                    button_href = coupon_button.get_attribute("href")
                    
                    if button_href and "linksynergy.com" in button_href:
                        # Extraer URL final de linksynergy
                        import urllib.parse
                        murl_match = re.search(r'murl=([^&]+)', button_href)
                        if murl_match:
                            final_url = urllib.parse.unquote(murl_match.group(1))
                            
                            if "udemy.com/course/" in final_url:
                                # Extraer información del curso
                                course_name = extract_course_name(final_url)
                                coupon_code = extract_coupon_code_from_url(final_url)
                                
                                if coupon_code:
                                    # Tomar screenshot
                                    screenshot_path = take_screenshot(driver, course_name, len(courses))
                                    
                                    # Construir URL completa
                                    if "couponCode=" in final_url:
                                        full_url = final_url
                                    else:
                                        full_url = f"{final_url}?couponCode={coupon_code}"
                                    
                                    course_data = {
                                        'title': course_name,
                                        'url': full_url,
                                        'coupon_code': coupon_code,
                                        'screenshot': screenshot_path,
                                        'source': 'CursosDev',
                                        'extracted_at': datetime.now().isoformat()
                                    }
                                    
                                    courses.append(course_data)
                                    processed_courses.add(href)
                                    
                                    print(f"Curso agregado: {course_name}")
                                    print(f"Cupon: {coupon_code}")
                                    print(f"Screenshot: {screenshot_path}")
                
                # Volver a la página principal
                driver.back()
                time.sleep(2)
                
            except Exception as e:
                print(f"Error procesando curso {i+1}: {e}")
                continue
        
        print(f"\nTotal de cursos extraidos: {len(courses)}")
        return courses
        
    except Exception as e:
        print(f"Error en extraccion: {e}")
        return []
    
    finally:
        if driver:
            driver.quit()

def create_html_page(courses):
    """Crear página HTML con los cursos"""
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cursos Gratuitos de Udemy - CursosDev</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .stats {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            color: white;
            text-align: center;
        }
        
        .courses-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }
        
        .course-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .course-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }
        
        .course-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid #eee;
        }
        
        .course-content {
            padding: 20px;
        }
        
        .course-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        
        .course-coupon {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 8px 15px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 15px;
        }
        
        .course-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            padding: 12px 25px;
            border-radius: 25px;
            display: inline-block;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 1rem;
        }
        
        .course-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .course-meta {
            margin-top: 15px;
            font-size: 0.9rem;
            color: #666;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            color: white;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .courses-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Cursos Gratuitos de Udemy</h1>
            <p>Descubre los mejores cursos gratuitos con cupones de CursosDev</p>
        </div>
        
        <div class="stats">
            <h2>📊 Estadísticas</h2>
            <p>Total de cursos disponibles: <strong>{total_courses}</strong></p>
            <p>Última actualización: <strong>{last_update}</strong></p>
        </div>
        
        <div class="courses-grid">
"""
    
    # Agregar cada curso
    for course in courses:
        screenshot_html = ""
        if course['screenshot'] and os.path.exists(course['screenshot']):
            # Convertir imagen a base64 para incrustarla
            try:
                with open(course['screenshot'], 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode()
                    screenshot_html = f'<img src="data:image/png;base64,{img_data}" alt="{course["title"]}" class="course-image">'
            except:
                screenshot_html = '<div class="course-image" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #666;">Sin imagen</div>'
        else:
            screenshot_html = '<div class="course-image" style="background: #f0f0f0; display: flex; align-items: center; justify-content: center; color: #666;">Sin imagen</div>'
        
        html_content += f"""
            <div class="course-card">
                {screenshot_html}
                <div class="course-content">
                    <h3 class="course-title">{course['title']}</h3>
                    <div class="course-coupon">🎫 Cupón: {course['coupon_code']}</div>
                    <a href="{course['url']}" target="_blank" class="course-button">Obtener Curso Gratis</a>
                    <div class="course-meta">
                        <p>📅 Extraído: {course['extracted_at'][:10]}</p>
                        <p>🔗 Fuente: {course['source']}</p>
                    </div>
                </div>
            </div>
        """
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>© 2024 Cursos Gratuitos de Udemy | Actualizado automáticamente</p>
            <p>Los cupones pueden tener tiempo limitado de validez</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Reemplazar placeholders
    html_content = html_content.replace('{total_courses}', str(len(courses)))
    html_content = html_content.replace('{last_update}', datetime.now().strftime('%d/%m/%Y %H:%M'))
    
    return html_content

def create_json_data(courses):
    """Crear archivo JSON con los datos de los cursos"""
    data = {
        'metadata': {
            'total_courses': len(courses),
            'last_update': datetime.now().isoformat(),
            'source': 'CursosDev',
            'note': 'Solo publicación web - Sin envío a WhatsApp'
        },
        'courses': courses
    }
    return json.dumps(data, indent=2, ensure_ascii=False)

def publish_to_github_pages():
    """Publicar en GitHub Pages - SOLO WEB"""
    print("Publicando en GitHub Pages...")
    print("SOLO PUBLICACION WEB - Sin envio a WhatsApp")
    
    # Extraer cursos
    courses = extract_courses_with_screenshots()
    
    if not courses:
        print("No se encontraron cursos para publicar")
        return False
    
    try:
        # Crear directorio docs si no existe (para GitHub Pages)
        docs_dir = "docs"
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        
        # Crear página HTML
        html_content = create_html_page(courses)
        with open(os.path.join(docs_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Crear archivo JSON con los datos
        json_data = create_json_data(courses)
        with open(os.path.join(docs_dir, "courses.json"), "w", encoding="utf-8") as f:
            f.write(json_data)
        
        # Crear README para GitHub Pages
        readme_content = f"""# Cursos Gratuitos de Udemy

Página web con cursos gratuitos de Udemy extraídos de CursosDev.

## 📊 Estadísticas

- **Total de cursos**: {len(courses)}
- **Última actualización**: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- **Fuente**: CursosDev
- **Nota**: Solo publicación web - Sin envío a WhatsApp

## 🎯 Cursos Disponibles

"""
        
        for i, course in enumerate(courses, 1):
            readme_content += f"{i}. **{course['title']}** - Cupón: `{course['coupon_code']}`\n"
        
        readme_content += """

## 🔗 Enlaces

- [Ver página web](https://tu-usuario.github.io/tu-repositorio/)
- [Datos en JSON](courses.json)

## 📝 Notas

- Los cupones pueden tener tiempo limitado de validez
- Actualizado automáticamente
- Extraído de CursosDev
- **Solo publicación web** - No se envía a WhatsApp
"""
        
        with open(os.path.join(docs_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"Archivos creados en directorio 'docs':")
        print(f"   - index.html (pagina principal)")
        print(f"   - courses.json (datos de cursos)")
        print(f"   - README.md (documentacion)")
        print(f"   - {len(courses)} screenshots")
        
        print("\nPara publicar en GitHub Pages:")
        print("1. Sube los archivos del directorio 'docs' a tu repositorio")
        print("2. Ve a Settings > Pages en tu repositorio")
        print("3. Selecciona 'Deploy from a branch'")
        print("4. Selecciona la rama 'main' y la carpeta '/docs'")
        print("5. Guarda los cambios")
        
        print("\nNOTA: Este script SOLO publica en GitHub Pages")
        print("   No envia mensajes a WhatsApp")
        
        return True
        
    except Exception as e:
        print(f"Error publicando: {e}")
        return False

def main():
    """Función principal"""
    print("Bot de Extraccion y Publicacion de Cursos")
    print("=" * 50)
    print("Este script extraera cursos de CursosDev con capturas de pantalla")
    print("y creara una pagina web para GitHub Pages")
    print("SOLO PUBLICACION WEB - Sin envio a WhatsApp")
    print("=" * 50)
    
    success = publish_to_github_pages()
    
    if success:
        print("\nProceso completado exitosamente!")
        print("Los archivos estan listos para ser subidos a GitHub Pages")
        print("Recuerda: Solo publicacion web, sin WhatsApp")
    else:
        print("\nError en el proceso")
        print("Revisa los logs para mas detalles")

if __name__ == "__main__":
    main() 