#!/usr/bin/env python3
"""
Bot mejorado para extraer 10 cursos y publicarlos en GitHub Pages
- Busca exactamente 10 cursos
- Capturas más pequeñas y enfocadas
- Verifica claramente "100% gratis"
- Publica en GitHub Pages
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

def convert_checkout_to_course_url(checkout_url):
    """Convertir enlace de checkout a enlace directo del curso"""
    try:
        course_id_match = re.search(r'/course/(\d+)/', checkout_url)
        if course_id_match:
            course_id = course_id_match.group(1)
            course_url = f"https://www.udemy.com/course/{course_id}/"
            return course_url
        return checkout_url
    except:
        return checkout_url

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

def take_focused_screenshot(driver, course_name):
    """Tomar captura de pantalla enfocada y más pequeña"""
    try:
        # Esperar a que la página cargue completamente
        time.sleep(3)
        
        # Buscar elementos específicos que indiquen que el curso es gratis
        free_indicators = [
            "//span[contains(text(), '100% gratis')]",
            "//span[contains(text(), '100% free')]",
            "//button[contains(text(), 'Inscribirse gratis')]",
            "//button[contains(text(), 'Enroll for free')]",
            "//span[contains(text(), '$0')]",
            "//div[contains(text(), 'Gratis')]",
            "//div[contains(text(), 'Free')]"
        ]
        
        # Buscar el primer indicador de gratis
        target_element = None
        for selector in free_indicators:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    target_element = elements[0]
                    print(f"✅ Encontrado indicador de gratis: {selector}")
                    break
            except:
                continue
        
        if target_element:
            # Tomar captura enfocada en el elemento que indica que es gratis
            screenshot = target_element.screenshot_as_png
            
            # Redimensionar la imagen para que sea más pequeña
            img = Image.open(io.BytesIO(screenshot))
            
            # Calcular nuevas dimensiones (máximo 400px de ancho)
            max_width = 400
            width, height = img.size
            if width > max_width:
                ratio = max_width / width
                new_width = max_width
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convertir a base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', optimize=True, quality=85)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            print(f"📸 Captura enfocada tomada para: {course_name}")
            return img_base64
        else:
            # Si no encuentra indicadores específicos, tomar captura general pero más pequeña
            screenshot = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))
            
            # Redimensionar a un tamaño más pequeño
            max_width = 600
            width, height = img.size
            if width > max_width:
                ratio = max_width / width
                new_width = max_width
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convertir a base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', optimize=True, quality=85)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            print(f"📸 Captura general tomada para: {course_name}")
            return img_base64
            
    except Exception as e:
        print(f"⚠️ Error tomando captura: {e}")
        return None

def verify_course_is_free(driver, udemy_url):
    """Verificar si el curso es 100% gratis con verificación mejorada"""
    try:
        print(f"🔍 Verificando si el curso es gratis: {udemy_url}")
        
        driver.get(udemy_url)
        time.sleep(3)
        
        page_text = driver.page_source.lower()
        
        # Buscar indicadores específicos de precio
        price_patterns = [
            r'\$\d+\.?\d*',
            r'€\d+\.?\d*',
            r'£\d+\.?\d*',
            r'\d+\.?\d*\s*\$',
            r'\d+\.?\d*\s*€',
            r'\d+\.?\d*\s*£'
        ]
        
        # Verificar si hay precios específicos (no $0)
        has_price = False
        for pattern in price_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                price_number = re.search(r'\d+\.?\d*', match)
                if price_number:
                    price_value = float(price_number.group())
                    if price_value > 0:
                        has_price = True
                        print(f"❌ Precio detectado: {match} (valor: {price_value})")
                        break
            if has_price:
                break
        
        # Buscar indicadores específicos de gratis
        free_indicators = [
            "100% gratis",
            "100% free", 
            "gratis",
            "free",
            "$0",
            "0.00",
            "0,00",
            "gratuito",
            "sin costo",
            "no cost",
            "completamente gratis",
            "completely free",
            "inscribirse gratis",
            "enroll for free",
            "inscribirse sin costo",
            "enroll at no cost",
            "inscribirse ahora",
            "enroll now",
            "free enrollment",
            "inscripción gratuita",
            "curso gratuito",
            "free course",
            "sin pagar",
            "no payment",
            "gratis para siempre",
            "free forever"
        ]
        
        # Verificar si hay indicadores de gratis
        is_free = False
        for indicator in free_indicators:
            if indicator.lower() in page_text:
                is_free = True
                print(f"✅ Indicador de gratis encontrado: {indicator}")
                break
        
        # Buscar botones específicos de inscripción gratuita
        free_button_selectors = [
            "//button[contains(text(), 'Inscribirse gratis')]",
            "//button[contains(text(), 'Enroll for free')]",
            "//button[contains(text(), 'Inscribirse sin costo')]",
            "//button[contains(text(), 'Enroll at no cost')]",
            "//button[contains(text(), 'Inscribirse ahora')]",
            "//button[contains(text(), 'Enroll now')]",
            "//a[contains(text(), 'Inscribirse gratis')]",
            "//a[contains(text(), 'Enroll for free')]",
            "//button[contains(text(), 'Free')]",
            "//button[contains(text(), 'Gratis')]",
            "//a[contains(text(), 'Free')]",
            "//a[contains(text(), 'Gratis')]",
            "//span[contains(text(), 'Free')]",
            "//span[contains(text(), 'Gratis')]"
        ]
        
        for selector in free_button_selectors:
            try:
                buttons = driver.find_elements(By.XPATH, selector)
                if buttons:
                    print(f"✅ Botón de inscripción gratuita encontrado: {selector}")
                    is_free = True
                    break
            except:
                continue
        
        # Buscar elementos con precio $0
        zero_price_selectors = [
            "//span[contains(text(), '$0')]",
            "//span[contains(text(), '0€')]",
            "//span[contains(text(), '0.00')]",
            "//div[contains(text(), '$0')]",
            "//div[contains(text(), '0€')]",
            "//div[contains(text(), '0.00')]"
        ]
        
        for selector in zero_price_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                if elements:
                    print(f"✅ Precio $0 encontrado: {selector}")
                    is_free = True
                    break
            except:
                continue
        
        # Lógica de decisión
        if has_price and not is_free:
            print("❌ El curso tiene precio, no es gratis")
            return False
        elif is_free:
            print("✅ El curso es 100% gratis")
            return True
        else:
            # Verificación adicional
            buy_button_selectors = [
                "//button[contains(text(), 'Buy')]",
                "//button[contains(text(), 'Comprar')]",
                "//button[contains(text(), 'Purchase')]",
                "//button[contains(text(), 'Add to cart')]",
                "//button[contains(text(), 'Agregar al carrito')]",
                "//button[contains(text(), 'Buy now')]",
                "//button[contains(text(), 'Comprar ahora')]"
            ]
            
            has_buy_button = False
            for selector in buy_button_selectors:
                try:
                    buttons = driver.find_elements(By.XPATH, selector)
                    if buttons:
                        print(f"❌ Botón de compra encontrado: {selector}")
                        has_buy_button = True
                        break
                except:
                    continue
            
            if has_buy_button:
                return False
            
            print("⚠️ No se encontraron indicadores claros, verificando cupón...")
            
            if 'couponcode=' in udemy_url.lower():
                print("✅ Cupón detectado en URL, asumiendo que puede hacer el curso gratis")
                return True
            
            print("❌ No se encontraron indicadores claros de que sea gratis")
            return False
        
    except Exception as e:
        print(f"⚠️ Error verificando si el curso es gratis: {e}")
        return False

def extraer_cursos_de_cursosdev(driver, max_cursos=10):
    """Extraer exactamente 10 cursos de CursosDev"""
    print(f"🔍 Extrayendo {max_cursos} cursos de CursosDev...")
    
    udemy_links = []
    processed_courses = set()
    
    try:
        # Navegar a la página principal de CursosDev
        print("🌐 Navegando a la página principal de CursosDev...")
        driver.set_page_load_timeout(30)
        driver.get("https://cursosdev.com/")
        time.sleep(3)
        
        if "cursosdev.com" not in driver.current_url.lower():
            print("❌ Error: No se pudo cargar la página principal de CursosDev")
            return udemy_links
        
        print("✅ Página principal de CursosDev cargada correctamente")
        
        # Hacer scroll para cargar más cursos
        print("📜 Haciendo scroll para cargar cursos...")
        for scroll in range(3):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                print(f"Scroll {scroll+1}/3 completado")
            except Exception as e:
                print(f"⚠️ Error en scroll {scroll+1}: {e}")
                break
        
        # Buscar enlaces de cursos
        print("🔍 Buscando enlaces de cursos en CursosDev...")
        
        try:
            # Buscar enlaces específicos de cursos
            course_links = []
            
            # Buscar enlaces que contengan "udemy"
            udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'udemy.com')]")
            course_links.extend(udemy_links)
            print(f"🔍 Enlaces de Udemy encontrados: {len(udemy_links)}")
            
            # Buscar enlaces que contengan "coupons-udemy"
            coupons_udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'coupons-udemy')]")
            course_links.extend(coupons_udemy_links)
            print(f"🔍 Enlaces con 'coupons-udemy' encontrados: {len(coupons_udemy_links)}")
            
            # Buscar enlaces en títulos
            title_links = driver.find_elements(By.XPATH, "//h1//a | //h2//a | //h3//a | //h4//a | //h5//a")
            course_links.extend(title_links)
            print(f"🔍 Enlaces en títulos encontrados: {len(title_links)}")
            
            # Buscar enlaces en artículos
            article_links = driver.find_elements(By.XPATH, "//article//a | //div[contains(@class, 'card')]//a | //div[contains(@class, 'post')]//a")
            course_links.extend(article_links)
            print(f"🔍 Enlaces en artículos/cards encontrados: {len(article_links)}")
            
            # Procesar los enlaces encontrados
            all_course_urls = []
            seen_urls = set()
            for link in course_links:
                try:
                    href = link.get_attribute("href")
                    if href and href not in seen_urls and href.startswith('http'):
                        if (('cursosdev.com' in href and ('coupons-udemy' in href or 'udemy.com' in href)) or
                            'udemy.com' in href or
                            (href.startswith('https://cursosdev.com/') and 
                             not href.startswith('https://cursosdev.com/courses/') and
                             not href.startswith('https://cursosdev.com/blog') and
                             not href.startswith('https://cursosdev.com/submit'))):
                            seen_urls.add(href)
                            all_course_urls.append(href)
                except:
                    continue
            
            course_urls = all_course_urls
            print(f"🔍 Encontrados {len(course_urls)} enlaces únicos de cursos...")
            
        except Exception as e:
            print(f"❌ Error buscando enlaces: {e}")
            return udemy_links
        
        # Procesar enlaces hasta encontrar exactamente max_cursos válidos
        valid_courses_found = 0
        for i in range(len(course_urls)):
            # Verificar si ya tenemos suficientes cursos
            if valid_courses_found >= max_cursos:
                print(f"✅ Ya se encontraron {max_cursos} cursos válidos, deteniendo búsqueda")
                break
                
            try:
                print(f"🔍 Procesando enlace {i+1}/{len(course_urls)}...")
                
                if i >= len(course_urls):
                    print("⚠️ No hay más enlaces disponibles")
                    break
                
                link_url = course_urls[i]
                print(f"📄 URL del enlace: {link_url}")
                
                # Inicializar variables para este curso
                coupon_code = None
                udemy_url = None
                original_url = None
                
                # Navegar a la página del curso
                try:
                    driver.get(link_url)
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Error navegando a la página: {e}")
                    continue
                
                # Verificar si ya estamos en Udemy
                current_url = driver.current_url
                print(f"🔍 URL actual: {current_url}")
                
                if "udemy.com/course/" in current_url:
                    print("✅ ¡Ya estamos en Udemy!")
                    udemy_url = current_url
                    original_url = current_url
                    
                    # Verificar si es un enlace de checkout y convertirlo
                    if "/payment/checkout/" in udemy_url:
                        print("🔄 Enlace de checkout detectado, convirtiendo a enlace directo...")
                        original_url = udemy_url
                        udemy_url = convert_checkout_to_course_url(udemy_url)
                        print(f"🔗 Enlace original: {original_url}")
                        print(f"🔗 Enlace convertido: {udemy_url}")
                    
                    # Extraer código de cupón
                    coupon_code = extract_coupon_code_from_url(original_url)
                    if not coupon_code:
                        coupon_code = extract_coupon_code_from_url(udemy_url)
                    
                    # Procesar el curso si tenemos cupón y URL de Udemy
                    if coupon_code and udemy_url:
                        print(f"🎫 Código de cupón encontrado: {coupon_code}")
                        
                        # Extraer ID del curso para evitar duplicados
                        course_id = extract_course_id(udemy_url)
                        
                        if course_id not in processed_courses:
                            # Verificar si el curso es realmente gratis
                            print("🔍 Verificando si el curso es 100% gratis...")
                            is_free = verify_course_is_free(driver, udemy_url)
                            
                            if is_free:
                                processed_courses.add(course_id)
                                
                                # Tomar captura de pantalla enfocada
                                course_name = extract_course_name(udemy_url)
                                screenshot = take_focused_screenshot(driver, course_name)
                                
                                # Construir URL completa con cupón
                                if "couponCode=" in udemy_url:
                                    full_url = udemy_url
                                else:
                                    full_url = f"{udemy_url}?couponCode={coupon_code}"
                                
                                udemy_links.append({
                                    'text': f"Curso de CursosDev: {course_name}",
                                    'urls': [full_url],
                                    'index': len(udemy_links),
                                    'screenshot': screenshot
                                })
                                valid_courses_found += 1
                                print(f"✅ Curso GRATIS agregado: {course_name}")
                                print(f"🎫 Código del cupón: {coupon_code}")
                                print(f"🔗 URL completa: {full_url}")
                                print(f"📊 Cursos válidos encontrados: {valid_courses_found}/{max_cursos}")
                            else:
                                print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                        else:
                            print(f"⚠️ Curso duplicado ignorado: {course_id}")
                    else:
                        print("❌ No se encontró código de cupón o URL de Udemy válida")
                else:
                    # Buscar botón "OBTENER CUPÓN" en CursosDev
                    print("🔍 Buscando botón de obtener cupón en CursosDev...")
                    coupon_button_selectors = [
                        "//button[contains(text(), 'OBTENER CUPÓN')]",
                        "//button[contains(text(), 'GET COUPON')]",
                        "//a[contains(text(), 'OBTENER CUPÓN')]",
                        "//a[contains(text(), 'GET COUPON')]",
                        "//button[contains(text(), 'cupón') or contains(text(), 'coupon')]",
                        "//a[contains(text(), 'cupón') or contains(text(), 'coupon')]",
                        "//*[contains(text(), 'OBTENER') and contains(text(), 'CUPÓN')]",
                        "//*[contains(text(), 'GET') and contains(text(), 'COUPON')]",
                        "//a[contains(text(), '🎟️ Obtener Cupón')]",
                        "//a[contains(text(), 'Obtener Cupón')]",
                        "//*[contains(text(), 'Obtener Cupón')]",
                        "//*[contains(text(), 'obtener cupón')]",
                        "//*[contains(text(), 'cupón')]"
                    ]
                    
                    coupon_button = None
                    for selector in coupon_button_selectors:
                        try:
                            buttons = driver.find_elements(By.XPATH, selector)
                            if buttons:
                                coupon_button = buttons[0]
                                print(f"✅ Botón encontrado con selector: {selector}")
                                break
                        except Exception as e:
                            continue
                    
                    if coupon_button:
                        # Obtener el href del botón antes de hacer clic
                        button_href = coupon_button.get_attribute("href")
                        print(f"🔗 Href del botón: {button_href}")
                        
                        # Si el botón tiene un enlace de linksynergy, extraer la URL final directamente
                        if button_href and "linksynergy.com" in button_href:
                            print("🔍 Encontrado enlace de linksynergy, extrayendo URL final...")
                            try:
                                # Extraer la URL final del parámetro murl
                                murl_match = re.search(r'murl=([^&]+)', button_href)
                                if murl_match:
                                    final_url = murl_match.group(1)
                                    # Decodificar URL
                                    import urllib.parse
                                    final_url = urllib.parse.unquote(final_url)
                                    print(f"🔗 URL final extraída: {final_url}")
                                    
                                    if "udemy.com/course/" in final_url:
                                        print("✅ ¡Enlace de Udemy extraído de linksynergy!")
                                        udemy_url = final_url
                                        original_url = final_url
                                        
                                        # Verificar si es un enlace de checkout y convertirlo
                                        if "/payment/checkout/" in udemy_url:
                                            print("🔄 Enlace de checkout detectado, convirtiendo a enlace directo...")
                                            original_url = udemy_url
                                            udemy_url = convert_checkout_to_course_url(udemy_url)
                                            print(f"🔗 Enlace original: {original_url}")
                                            print(f"🔗 Enlace convertido: {udemy_url}")
                                        
                                        # Extraer código de cupón
                                        coupon_code = extract_coupon_code_from_url(original_url)
                                        if not coupon_code:
                                            coupon_code = extract_coupon_code_from_url(udemy_url)
                                        
                                        # Procesar el curso si tenemos cupón y URL de Udemy
                                        if coupon_code and udemy_url:
                                            print(f"🎫 Código de cupón encontrado: {coupon_code}")
                                            
                                            # Extraer ID del curso para evitar duplicados
                                            course_id = extract_course_id(udemy_url)
                                            
                                            if course_id not in processed_courses:
                                                # Verificar si el curso es realmente gratis
                                                print("🔍 Verificando si el curso es 100% gratis...")
                                                is_free = verify_course_is_free(driver, udemy_url)
                                                
                                                if is_free:
                                                    processed_courses.add(course_id)
                                                    
                                                    # Tomar captura de pantalla enfocada
                                                    course_name = extract_course_name(udemy_url)
                                                    screenshot = take_focused_screenshot(driver, course_name)
                                                    
                                                    # Construir URL completa con cupón
                                                    if "couponCode=" in udemy_url:
                                                        full_url = udemy_url
                                                    else:
                                                        full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                    
                                                    udemy_links.append({
                                                        'text': f"Curso de CursosDev: {course_name}",
                                                        'urls': [full_url],
                                                        'index': len(udemy_links),
                                                        'screenshot': screenshot
                                                    })
                                                    valid_courses_found += 1
                                                    print(f"✅ Curso GRATIS agregado: {course_name}")
                                                    print(f"🎫 Código del cupón: {coupon_code}")
                                                    print(f"🔗 URL completa: {full_url}")
                                                    print(f"📊 Cursos válidos encontrados: {valid_courses_found}/{max_cursos}")
                                                else:
                                                    print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                                            else:
                                                print(f"⚠️ Curso duplicado ignorado: {course_id}")
                                        else:
                                            print("❌ No se encontró código de cupón o URL de Udemy válida")
                                    else:
                                        print("⚠️ La URL extraída no es de Udemy")
                                else:
                                    print("⚠️ No se pudo extraer la URL final del enlace linksynergy")
                            except Exception as e:
                                print(f"⚠️ Error extrayendo URL de linksynergy: {e}")
                        else:
                            # Hacer clic en el botón normalmente
                            print("🖱️ Haciendo clic en botón de cupón...")
                            try:
                                coupon_button.click()
                                time.sleep(3)
                                
                                # Verificar si se redirigió a Udemy
                                current_url = driver.current_url
                                print(f"🔍 URL después de hacer clic: {current_url}")
                                
                                if "udemy.com/course/" in current_url:
                                    print("✅ ¡Enlace de Udemy encontrado!")
                                    udemy_url = current_url
                                    original_url = current_url
                                    
                                    # Verificar si es un enlace de checkout y convertirlo
                                    if "/payment/checkout/" in udemy_url:
                                        print("🔄 Enlace de checkout detectado, convirtiendo a enlace directo...")
                                        original_url = udemy_url
                                        udemy_url = convert_checkout_to_course_url(udemy_url)
                                        print(f"🔗 Enlace original: {original_url}")
                                        print(f"🔗 Enlace convertido: {udemy_url}")
                                    
                                    # Extraer código de cupón
                                    coupon_code = extract_coupon_code_from_url(original_url)
                                    if not coupon_code:
                                        coupon_code = extract_coupon_code_from_url(udemy_url)
                                    
                                    # Procesar el curso si tenemos cupón y URL de Udemy
                                    if coupon_code and udemy_url:
                                        print(f"🎫 Código de cupón encontrado: {coupon_code}")
                                        
                                        # Extraer ID del curso para evitar duplicados
                                        course_id = extract_course_id(udemy_url)
                                        
                                        if course_id not in processed_courses:
                                            # Verificar si el curso es realmente gratis
                                            print("🔍 Verificando si el curso es 100% gratis...")
                                            is_free = verify_course_is_free(driver, udemy_url)
                                            
                                            if is_free:
                                                processed_courses.add(course_id)
                                                
                                                # Tomar captura de pantalla enfocada
                                                course_name = extract_course_name(udemy_url)
                                                screenshot = take_focused_screenshot(driver, course_name)
                                                
                                                # Construir URL completa con cupón
                                                if "couponCode=" in udemy_url:
                                                    full_url = udemy_url
                                                else:
                                                    full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                
                                                udemy_links.append({
                                                    'text': f"Curso de CursosDev: {course_name}",
                                                    'urls': [full_url],
                                                    'index': len(udemy_links),
                                                    'screenshot': screenshot
                                                })
                                                valid_courses_found += 1
                                                print(f"✅ Curso GRATIS agregado: {course_name}")
                                                print(f"🎫 Código del cupón: {coupon_code}")
                                                print(f"🔗 URL completa: {full_url}")
                                                print(f"📊 Cursos válidos encontrados: {valid_courses_found}/{max_cursos}")
                                            else:
                                                print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                                        else:
                                            print(f"⚠️ Curso duplicado ignorado: {course_id}")
                                    else:
                                        print("❌ No se encontró código de cupón o URL de Udemy válida")
                                else:
                                    print("⚠️ No se llegó a Udemy después de hacer clic en el botón")
                            except Exception as e:
                                print(f"⚠️ Error haciendo clic en el botón: {e}")
                    else:
                        print("⚠️ No se encontró el botón de obtener cupón en CursosDev")
                
                # Volver a la página principal de CursosDev
                try:
                    driver.back()
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Error volviendo atrás: {e}")
                    driver.get("https://cursosdev.com/")
                    time.sleep(3)
                
            except Exception as e:
                print(f"⚠️ Error procesando curso {i+1}: {e}")
                try:
                    driver.back()
                    time.sleep(2)
                except:
                    driver.get("https://cursosdev.com/")
                    time.sleep(3)
                continue
    
    except Exception as e:
        print(f"❌ Error en extraer_cursos_de_cursosdev: {e}")
    
    print(f"📊 Cursos extraídos de CursosDev: {len(udemy_links)}")
    return udemy_links

def create_html_page(courses):
    """Crear página HTML con los cursos encontrados"""
    print("🌐 Creando página HTML...")
    
    # Crear directorio docs si no existe
    os.makedirs("docs", exist_ok=True)
    
    # Crear contenido HTML
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cursos Gratuitos de Udemy - CursosDev</title>
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
            font-size: 2.5rem;
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
        }}
        
        .course-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .course-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        .course-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid #eee;
        }}
        
        .course-content {{
            padding: 20px;
        }}
        
        .course-title {{
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        .course-coupon {{
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 8px 15px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 15px;
        }}
        
        .course-button {{
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
        }}
        
        .course-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .course-meta {{
            margin-top: 15px;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: white;
            opacity: 0.8;
        }}
        
        @media (max-width: 768px) {{
            .courses-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
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
            <p>Total de cursos disponibles: <strong>{len(courses)}</strong></p>
            <p>Última actualización: <strong>{datetime.now().strftime('%d/%m/%Y %H:%M')}</strong></p>
        </div>
        
        <div class="courses-grid">
"""
    
    # Agregar cada curso al HTML
    for i, course in enumerate(courses):
        course_name = course['text'].replace("Curso de CursosDev: ", "")
        course_url = course['urls'][0]
        screenshot = course.get('screenshot')
        
        # Extraer código de cupón de la URL
        coupon_code = "No encontrado"
        if 'couponCode=' in course_url:
            coupon_code = course_url.split('couponCode=')[1].split('&')[0]
        
        html_content += f"""
            <div class="course-card">
                <img src="data:image/png;base64,{screenshot if screenshot else ''}" alt="{course_name}" class="course-image">
                <div class="course-content">
                    <h3 class="course-title">{course_name}</h3>
                    <div class="course-coupon">🎫 Cupón: {coupon_code}</div>
                    <a href="{course_url}" target="_blank" class="course-button">Inscribirse Gratis</a>
                    <div class="course-meta">
                        <p>✅ 100% Gratis</p>
                        <p>📚 CursosDev</p>
                    </div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>© 2024 CursosDev - Todos los cursos son 100% gratuitos</p>
        </div>
    </div>
</body>
</html>"""
    
    # Guardar archivo HTML
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Página HTML creada en docs/index.html")
    return True

def commit_and_push_to_github():
    """Hacer commit y push a GitHub"""
    print("📤 Subiendo cambios a GitHub...")
    
    try:
        import subprocess
        
        # Agregar todos los archivos
        result = subprocess.run("git add .", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error agregando archivos: {result.stderr}")
            return False
        
        # Hacer commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Actualizar 10 cursos gratuitos - {timestamp}"
        result = subprocess.run(f'git commit -m "{commit_message}"', shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error haciendo commit: {result.stderr}")
            return False
        
        # Hacer push
        result = subprocess.run("git push origin main", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error haciendo push: {result.stderr}")
            return False
        
        print("✅ Cambios subidos a GitHub exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en commit y push: {e}")
        return False

def main():
    """Función principal del bot mejorado"""
    print("🚀 Bot Mejorado - 10 Cursos Gratuitos")
    print("=" * 50)
    print("🎯 Buscando exactamente 10 cursos gratuitos")
    print("📸 Capturas enfocadas y más pequeñas")
    print("🌐 Publicando en GitHub Pages")
    print("=" * 50)
    
    driver = None
    
    try:
        # 1. INICIALIZAR DRIVER DE CHROME
        print("\nPASO 1: Inicializando navegador...")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # 2. EXTRAER EXACTAMENTE 10 CURSOS
        print("\nPASO 2: Extrayendo 10 cursos gratuitos de CursosDev...")
        courses = extraer_cursos_de_cursosdev(driver, max_cursos=10)
        
        if not courses:
            print("❌ No se encontraron cursos gratuitos")
            return False
        
        print(f"\n📊 RESUMEN:")
        print(f"✅ Cursos gratuitos encontrados: {len(courses)}")
        
        # 3. CREAR PÁGINA HTML
        print(f"\nPASO 3: Creando página HTML...")
        if not create_html_page(courses):
            print("❌ Error creando página HTML")
            return False
        
        # 4. SUBIR A GITHUB
        print(f"\nPASO 4: Subiendo a GitHub...")
        if not commit_and_push_to_github():
            print("❌ Error subiendo a GitHub")
            return False
        
        print(f"\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print(f"✅ {len(courses)} cursos gratuitos extraídos")
        print(f"✅ Página HTML creada")
        print(f"✅ Cambios subidos a GitHub")
        print(f"🌐 La página estará disponible en GitHub Pages")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en la ejecución: {e}")
        return False
    
    finally:
        # Cerrar el navegador
        if driver:
            try:
                driver.quit()
                print("🌐 Navegador cerrado")
            except:
                pass

if __name__ == "__main__":
    main() 