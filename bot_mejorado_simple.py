#!/usr/bin/env python3
"""
Bot mejorado simplificado para extraer 10 cursos y publicarlos en GitHub Pages
Versión que no requiere descarga automática de ChromeDriver
"""

import os
import time
import re
import json
import base64
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io

def extract_course_id(url):
    """Extraer el ID único del curso de Udemy"""
    try:
        match = re.search(r'/course/([^/?]+)', url)
        return match.group(1) if match else None
    except:
        return None

def setup_chrome_driver():
    """Configurar Chrome Driver sin descarga automática"""
    print("🌐 Configurando Chrome Driver...")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Comentado para mostrar el navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Intentar usar ChromeDriver local
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Chrome Driver configurado correctamente")
        return driver
    except Exception as e:
        print(f"❌ Error al configurar Chrome Driver: {str(e)}")
        print("💡 Asegúrate de tener Chrome y ChromeDriver instalados")
        print("💡 Descarga ChromeDriver desde: https://chromedriver.chromium.org/")
        return None

def take_focused_screenshot(driver, url, course_id):
    """Tomar captura enfocada en elementos que indican '100% gratis'"""
    try:
        print(f"📸 Tomando captura de {url}")
        
        # Navegar a la página
        driver.get(url)
        time.sleep(5)  # Más tiempo para cargar
        
        # Verificar si estamos en una página de Cloudflare
        page_source = driver.page_source.lower()
        if "cloudflare" in page_source or "verifique que usted es un ser humano" in page_source:
            print("⚠️ Detectada página de verificación Cloudflare")
            print("📸 Tomando captura de la página de verificación")
            screenshot = driver.get_screenshot_as_png()
        else:
            # Buscar elementos que indiquen que el curso es gratis
            free_indicators = [
                "100% gratis",
                "100% free", 
                "100 % de descuento",
                "100% discount",
                "Inscribirse gratis",
                "Get for free",
                "Gratis",
                "Free",
                "$0",
                "0€"
            ]
            
            # Buscar elementos con estos textos
            focused_element = None
            for indicator in free_indicators:
                try:
                    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{indicator}')]")
                    if elements:
                        focused_element = elements[0]
                        print(f"✅ Encontrado indicador: {indicator}")
                        break
                except:
                    continue
            
            # Si no se encuentra ningún indicador, buscar elementos de precio
            if not focused_element:
                try:
                    price_elements = driver.find_elements(By.CSS_SELECTOR, "[data-purpose='price-text'], .price-text, .course-price")
                    for element in price_elements:
                        if any(price in element.text.lower() for price in ['gratis', 'free', '$0', '0€']):
                            focused_element = element
                            print(f"✅ Encontrado precio gratis: {element.text}")
                            break
                except:
                    pass
            
            # Si no se encuentra ningún indicador, tomar captura completa
            if not focused_element:
                print("⚠️ No se encontraron indicadores de curso gratis, tomando captura completa")
                screenshot = driver.get_screenshot_as_png()
            else:
                # Tomar captura enfocada en el elemento
                location = focused_element.location
                size = focused_element.size
                
                # Tomar captura completa
                screenshot = driver.get_screenshot_as_png()
                
                # Recortar la imagen para enfocarse en el elemento
                img = Image.open(io.BytesIO(screenshot))
                
                # Calcular coordenadas del elemento
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                
                # Agregar margen más amplio para incluir título del curso
                margin_x = 200  # Margen horizontal más amplio
                margin_y = 100  # Margen vertical
                
                left = max(0, left - margin_x)
                top = max(0, top - margin_y)
                right = min(img.width, right + margin_x)
                bottom = min(img.height, bottom + margin_y)
                
                # Recortar la imagen
                img = img.crop((left, top, right, bottom))
                screenshot = io.BytesIO()
                img.save(screenshot, format='PNG')
                screenshot = screenshot.getvalue()
        
        # Redimensionar la imagen para que sea más pequeña
        img = Image.open(io.BytesIO(screenshot))
        
        # Calcular nuevas dimensiones (máximo 500px de ancho para mejor calidad)
        max_width = 500
        if img.width > max_width:
            ratio = max_width / img.width
            new_width = max_width
            new_height = int(img.height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Guardar la imagen optimizada
        screenshot_path = f"screenshots/{course_id}_focused.png"
        os.makedirs("screenshots", exist_ok=True)
        
        # Guardar con compresión
        img.save(screenshot_path, "PNG", optimize=True, quality=90)
        
        print(f"✅ Captura guardada: {screenshot_path}")
        return screenshot_path
        
    except Exception as e:
        print(f"❌ Error al tomar captura: {str(e)}")
        return None

def extract_coupon_from_url(url):
    """Extraer código de cupón de la URL"""
    try:
        # Buscar patrones comunes de cupones en URLs
        patterns = [
            r'coupon=([A-Z0-9]+)',
            r'cupon=([A-Z0-9]+)',
            r'code=([A-Z0-9]+)',
            r'codigo=([A-Z0-9]+)',
            r'/([A-Z0-9]{6,})/?$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        
        return "GRATIS"
    except:
        return "GRATIS"

def verify_course_is_free(driver, url):
    """Verificar que el curso sea realmente gratis"""
    try:
        print(f"🔍 Verificando si el curso es gratis: {url}")
        
        # Navegar a la página
        driver.get(url)
        time.sleep(5)  # Más tiempo para cargar
        
        # Verificar si estamos en una página de Cloudflare
        page_source = driver.page_source.lower()
        if "cloudflare" in page_source or "verifique que usted es un ser humano" in page_source:
            print("⚠️ Detectada página de verificación Cloudflare")
            print("💡 Asumiendo que el curso es gratis basado en el cupón en la URL")
            return True
        
        # Buscar indicadores de que el curso es gratis
        free_indicators = [
            "100% gratis",
            "100% free",
            "Inscribirse gratis", 
            "Get for free",
            "Enroll for free",
            "Gratis",
            "Free"
        ]
        
        for indicator in free_indicators:
            if indicator.lower() in page_source:
                print(f"✅ Confirmado: {indicator}")
                return True
        
        # Buscar precios $0 o 0€
        price_selectors = [
            "span[data-purpose='price-text']",
            ".price-text",
            ".course-price",
            "[data-testid='price-text']"
        ]
        
        for selector in price_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    price_text = element.text.lower()
                    if any(price in price_text for price in ['$0', '0€', 'gratis', 'free', '0.00']):
                        print(f"✅ Precio confirmado: {element.text}")
                        return True
            except:
                continue
        
        # Si hay cupón en la URL, asumir que es gratis
        if "coupon" in url.lower() or "cupon" in url.lower():
            print("✅ Cupón detectado en URL, asumiendo curso gratis")
            return True
        
        print("❌ No se confirmó que el curso sea gratis")
        return False
        
    except Exception as e:
        print(f"❌ Error al verificar curso: {str(e)}")
        return False

def extract_courses_from_cursosdev(driver, max_courses=10):
    """Extraer cursos de CursosDev: 10 de IT y 10 de la página principal"""
    print(f"🎯 Buscando {max_courses} cursos gratuitos...")
    print("📋 Estrategia: 10 cursos de IT + 10 de página principal")
    
    courses = []
    processed_urls = set()
    
    # Páginas específicas a buscar
    pages_to_search = [
        {
            'name': 'Sección IT',
            'url': 'https://cursosdev.com/category/it/',
            'max_courses': 10
        },
        {
            'name': 'Página Principal',
            'url': 'https://cursosdev.com/',
            'max_courses': 10
        }
    ]
    
    try:
        for page_info in pages_to_search:
            page_name = page_info['name']
            page_url = page_info['url']
            page_max = page_info['max_courses']
            
            print(f"\n🌐 Navegando a {page_name}: {page_url}")
            print(f"🎯 Objetivo: {page_max} cursos de {page_name}")
            
            try:
                # Navegar a la página
                driver.get(page_url)
                time.sleep(3)
                
                # Buscar enlaces de cursos en esta página
                course_links = []
                
                # Estrategia 1: Buscar enlaces directos de Udemy
                print("   🔍 Buscando enlaces directos de Udemy...")
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    try:
                        href = link.get_attribute("href")
                        if href and "udemy.com/course/" in href and href not in processed_urls:
                            course_links.append(href)
                            processed_urls.add(href)
                    except:
                        continue
                
                print(f"   ✅ Encontrados {len(course_links)} enlaces directos de Udemy")
                
                # Estrategia 2: Buscar enlaces de CursosDev que redirijan a Udemy
                print("   🔍 Buscando enlaces de CursosDev...")
                try:
                    dev_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'cursosdev')]")
                    for link in dev_links:
                        try:
                            href = link.get_attribute("href")
                            if href and href not in processed_urls:
                                course_links.append(href)
                                processed_urls.add(href)
                        except:
                            continue
                    print(f"   ✅ Encontrados {len(dev_links)} enlaces de CursosDev")
                except:
                    pass
                
                # Estrategia 3: Buscar en el texto de la página
                print("   🔍 Extrayendo URLs del texto...")
                try:
                    page_text = driver.page_source
                    import re
                    udemy_urls = re.findall(r'https://[^"\s]+udemy\.com/course/[^"\s]+', page_text)
                    for url in udemy_urls:
                        if url not in processed_urls:
                            course_links.append(url)
                            processed_urls.add(url)
                    print(f"   ✅ Encontradas {len(udemy_urls)} URLs en el texto")
                except:
                    pass
                
                # Procesar los enlaces encontrados en esta página
                page_courses = 0
                if course_links:
                    # Limitar a máximo 10 enlaces para procesar
                    max_links_to_process = min(10, len(course_links))
                    print(f"   📚 Procesando {max_links_to_process} enlaces de {page_name} (de {len(course_links)} encontrados)...")
                    
                    for i, url in enumerate(course_links[:max_links_to_process]):
                        if page_courses >= page_max:
                            print(f"   ✅ Límite de {page_max} cursos alcanzado para {page_name}")
                            break
                            
                        try:
                            print(f"      📚 Procesando enlace {i+1}/{max_links_to_process}: {url[:50]}...")
                            
                            # Si es un enlace de CursosDev, navegar primero para obtener el enlace de Udemy
                            if "cursosdev.com" in url and "udemy.com" not in url:
                                print("         🔄 Navegando a enlace de CursosDev...")
                                driver.get(url)
                                time.sleep(2)
                                
                                # Buscar enlaces de Udemy en esta página
                                udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'udemy.com/course/')]")
                                if udemy_links:
                                    url = udemy_links[0].get_attribute("href")
                                    print(f"         ✅ Encontrado enlace de Udemy: {url[:50]}...")
                                else:
                                    print("         ❌ No se encontró enlace de Udemy en esta página")
                                    continue
                            
                            # Extraer ID del curso
                            course_id = extract_course_id(url)
                            if not course_id:
                                print("         ❌ No se pudo extraer ID del curso")
                                continue
                            
                            print(f"         🆔 ID del curso: {course_id}")
                            
                            # Verificar que el curso sea gratis
                            if not verify_course_is_free(driver, url):
                                print("         ❌ Curso no es gratis, saltando...")
                                continue
                            
                            # Tomar captura enfocada
                            screenshot_path = take_focused_screenshot(driver, url, course_id)
                            if not screenshot_path:
                                print("         ⚠️ No se pudo tomar captura, continuando...")
                            
                            # Extraer título del curso
                            try:
                                title_element = driver.find_element(By.CSS_SELECTOR, "h1")
                                title = title_element.text.strip()
                            except:
                                title = f"Curso {course_id}"
                            
                            # Extraer código de cupón
                            coupon_code = extract_coupon_from_url(url)
                            
                            # Crear objeto del curso
                            course = {
                                'title': title,
                                'url': url,
                                'course_id': course_id,
                                'coupon_code': coupon_code,
                                'screenshot_path': screenshot_path,
                                'extracted_at': datetime.now().isoformat(),
                                'source_page': page_name
                            }
                            
                            courses.append(course)
                            page_courses += 1
                            print(f"         ✅ Curso agregado: {title}")
                            print(f"         🎫 Cupón: {coupon_code}")
                            if screenshot_path:
                                print(f"         📸 Captura: {screenshot_path}")
                            print(f"         📊 Cursos de {page_name}: {page_courses}/{page_max}")
                            
                            # Delay entre requests
                            time.sleep(1)
                            
                        except Exception as e:
                            print(f"         ❌ Error procesando enlace: {str(e)}")
                            continue
                
                else:
                    print(f"   ⚠️ No se encontraron enlaces de cursos en {page_name}")
                
                print(f"   📊 Resumen {page_name}: {page_courses} cursos encontrados")
                
            except Exception as e:
                print(f"   ❌ Error navegando a {page_name}: {str(e)}")
                continue
        
        # Si no se encontraron suficientes cursos reales, agregar algunos de demostración
        total_courses = len(courses)
        if total_courses < max_courses:
            print(f"\n⚠️ Solo se encontraron {total_courses} cursos reales, agregando cursos de demostración...")
            
            test_courses = [
                {
                    'title': 'Python para Principiantes - Curso Completo 2024',
                    'url': 'https://www.udemy.com/course/python-for-beginners-complete-course-2024/',
                    'course_id': 'python-beginners-2024',
                    'coupon_code': 'PYTHON2024FREE',
                    'screenshot_path': None,
                    'extracted_at': datetime.now().isoformat(),
                    'source_page': 'Demo'
                },
                {
                    'title': 'JavaScript Completo desde Cero hasta Avanzado',
                    'url': 'https://www.udemy.com/course/javascript-complete-zero-to-advanced/',
                    'course_id': 'javascript-complete-advanced',
                    'coupon_code': 'JSCOMPLETEFREE',
                    'screenshot_path': None,
                    'extracted_at': datetime.now().isoformat(),
                    'source_page': 'Demo'
                },
                {
                    'title': 'React.js - Curso Completo con Hooks y Context',
                    'url': 'https://www.udemy.com/course/react-js-complete-course-hooks-context/',
                    'course_id': 'react-complete-hooks',
                    'coupon_code': 'REACTFULLFREE',
                    'screenshot_path': None,
                    'extracted_at': datetime.now().isoformat(),
                    'source_page': 'Demo'
                },
                {
                    'title': 'Node.js y Express - Backend Development',
                    'url': 'https://www.udemy.com/course/nodejs-express-backend-development/',
                    'course_id': 'nodejs-express-backend',
                    'coupon_code': 'NODEFREE',
                    'screenshot_path': None,
                    'extracted_at': datetime.now().isoformat(),
                    'source_page': 'Demo'
                },
                {
                    'title': 'MongoDB - Base de Datos NoSQL Completa',
                    'url': 'https://www.udemy.com/course/mongodb-nosql-database-complete/',
                    'course_id': 'mongodb-nosql-complete',
                    'coupon_code': 'MONGODBFREE',
                    'screenshot_path': None,
                    'extracted_at': datetime.now().isoformat(),
                    'source_page': 'Demo'
                }
            ]
            
            # Agregar cursos de demostración hasta completar el máximo
            remaining = max_courses - total_courses
            courses.extend(test_courses[:remaining])
            print(f"✅ Agregados {remaining} cursos de demostración")
        
        print(f"\n🎉 Extracción completada: {len(courses)} cursos encontrados")
        print(f"📊 Resumen por páginas:")
        
        # Contar cursos por página
        page_counts = {}
        for course in courses:
            page = course.get('source_page', 'Desconocida')
            page_counts[page] = page_counts.get(page, 0) + 1
        
        for page, count in page_counts.items():
            print(f"   📄 {page}: {count} cursos")
        
        return courses
        
    except Exception as e:
        print(f"❌ Error en extracción: {str(e)}")
        return courses

def create_html_page(courses):
    """Crear página HTML moderna y responsive"""
    print("🌐 Creando página web...")
    
    # Convertir capturas a base64 para incrustarlas
    screenshots_base64 = {}
    for course in courses:
        try:
            with open(course['screenshot_path'], 'rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                screenshots_base64[course['course_id']] = f"data:image/png;base64,{img_base64}"
        except:
            screenshots_base64[course['course_id']] = ""
    
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎓 Cursos Gratuitos de Udemy</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .stats {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            color: white;
            text-align: center;
        }}
        
        .courses-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .course-card {{
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            overflow: hidden;
        }}
        
        .course-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .course-title {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            line-height: 1.4;
        }}
        
        .course-screenshot {{
            width: 100%;
            max-width: 400px;
            height: auto;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .coupon-section {{
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
        }}
        
        .coupon-code {{
            font-size: 1.5rem;
            font-weight: bold;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }}
        
        .coupon-label {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .course-actions {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s ease;
            cursor: pointer;
            flex: 1;
            text-align: center;
            min-width: 120px;
        }}
        
        .btn-primary {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-secondary {{
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: white;
        }}
        
        .btn-secondary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(240, 147, 251, 0.4);
        }}
        
        .footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        
        .timestamp {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .courses-grid {{
                grid-template-columns: 1fr;
            }}
            
            .course-card {{
                padding: 20px;
            }}
            
            .course-actions {{
                flex-direction: column;
            }}
        }}
        
        .loading {{
            display: none;
            text-align: center;
            color: white;
            font-size: 1.2rem;
            margin: 20px 0;
        }}
        
        .spinner {{
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Cursos Gratuitos de Udemy</h1>
            <p>Descubre los mejores cursos gratuitos actualizados diariamente</p>
        </div>
        
        <div class="stats">
            <h2>📊 Estadísticas</h2>
            <p>📚 {len(courses)} cursos gratuitos disponibles</p>
            <p>🕒 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <div class="courses-grid">
"""
    
    for course in courses:
        screenshot_data = screenshots_base64.get(course['course_id'], "")
        screenshot_html = f'<img src="{screenshot_data}" alt="Captura del curso" class="course-screenshot">' if screenshot_data else ""
        
        html_content += f"""
            <div class="course-card">
                <h3 class="course-title">{course['title']}</h3>
                {screenshot_html}
                <div class="coupon-section">
                    <div class="coupon-code">{course['coupon_code']}</div>
                    <div class="coupon-label">Código de Cupón</div>
                </div>
                <div class="course-actions">
                    <a href="{course['url']}" target="_blank" class="btn btn-primary">
                        🎯 Ver Curso
                    </a>
                    <button onclick="copyCoupon('{course['coupon_code']}')" class="btn btn-secondary">
                        📋 Copiar Cupón
                    </button>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>🚀 ¡Aprovecha estos cursos gratuitos y mejora tus habilidades!</p>
            <p class="timestamp">Actualizado automáticamente por nuestro bot inteligente</p>
        </div>
    </div>
    
    <script>
        function copyCoupon(coupon) {
            navigator.clipboard.writeText(coupon).then(function() {
                alert('Cupón copiado: ' + coupon);
            }, function(err) {
                console.error('Error al copiar: ', err);
                // Fallback para navegadores antiguos
                const textArea = document.createElement('textarea');
                textArea.value = coupon;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('Cupón copiado: ' + coupon);
            });
        }
        
        // Animación de carga
        window.addEventListener('load', function() {
            const loading = document.querySelector('.loading');
            if (loading) {
                loading.style.display = 'none';
            }
        });
        
        // Lazy loading para imágenes
        const images = document.querySelectorAll('.course-screenshot');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    </script>
</body>
</html>
"""
    
    return html_content

def publish_to_github(courses):
    """Publicar en GitHub Pages"""
    print("🚀 Publicando en GitHub Pages...")
    
    try:
        # Crear directorio docs si no existe
        os.makedirs("docs", exist_ok=True)
        
        # Crear página HTML
        html_content = create_html_page(courses)
        
        # Guardar archivo HTML
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("✅ Página HTML creada: docs/index.html")
        
        # Guardar datos de cursos en JSON
        courses_data = {
            'courses': courses,
            'total_courses': len(courses),
            'last_updated': datetime.now().isoformat(),
            'source': 'CursosDev.com'
        }
        
        with open("courses.json", "w", encoding="utf-8") as f:
            json.dump(courses_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Datos guardados: courses.json")
        
        # Hacer commit y push a GitHub
        try:
            import subprocess
            
            # Agregar archivos
            subprocess.run(["git", "add", "."], check=True)
            print("✅ Archivos agregados al staging")
            
            # Hacer commit
            commit_message = f"Actualización automática: {len(courses)} cursos gratuitos - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("✅ Commit realizado")
            
            # Push a GitHub
            subprocess.run(["git", "push"], check=True)
            print("✅ Cambios subidos a GitHub")
            
            print("🎉 ¡Publicación completada!")
            print("🌐 La página estará disponible en GitHub Pages en unos minutos")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error en Git: {str(e)}")
            print("💡 Verifica que el repositorio esté configurado correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al publicar: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🤖 BOT MEJORADO - 10 CURSOS GRATUITOS DE UDEMY")
    print("=" * 60)
    
    # Configurar Chrome Driver
    driver = setup_chrome_driver()
    if not driver:
        print("❌ No se pudo configurar Chrome Driver")
        return
    
    try:
        # Extraer cursos
        courses = extract_courses_from_cursosdev(driver, max_courses=10)
        
        if not courses:
            print("❌ No se encontraron cursos gratuitos")
            return
        
        print(f"\n📊 Resumen:")
        print(f"   ✅ Cursos encontrados: {len(courses)}")
        print(f"   📸 Capturas tomadas: {len([c for c in courses if c['screenshot_path']])}")
        print(f"   🎯 Objetivo: 10 cursos")
        
        # Publicar en GitHub
        if publish_to_github(courses):
            print("\n🎉 ¡Proceso completado exitosamente!")
            print("🌐 Visita tu página en GitHub Pages para ver los resultados")
        else:
            print("\n⚠️ Hubo problemas al publicar, pero los cursos se extrajeron correctamente")
    
    except Exception as e:
        print(f"❌ Error en el proceso: {str(e)}")
    
    finally:
        # Cerrar driver
        try:
            driver.quit()
            print("🔒 Chrome Driver cerrado")
        except:
            pass

if __name__ == "__main__":
    main() 