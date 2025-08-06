#!/usr/bin/env python3
"""
Bot simplificado para extraer cursos con cupones de Coupon Scorpion y enviarlos por WhatsApp
"""
import os
import time
import re
from datetime import datetime
from send_cursos_sin_emojis import enviar_cursos_sin_emojis
from selenium.webdriver.common.by import By

def extract_course_id(url):
    """Extraer el ID único del curso de Udemy"""
    try:
        # Buscar el patrón /course/nombre-del-curso/ o /course/ID/
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
            # Si es un ID numérico, usar nombre genérico
            if course_id.isdigit():
                return f"Curso de Udemy (ID: {course_id})"
            # Convertir guiones y guiones bajos a espacios
            course_name = course_id.replace('-', ' ').replace('_', ' ')
            # Capitalizar palabras
            course_name = ' '.join(word.capitalize() for word in course_name.split())
            return course_name
        return "Curso de Udemy"
    except:
        return "Curso de Udemy"

def convert_checkout_to_course_url(checkout_url):
    """Convertir enlace de checkout a enlace directo del curso"""
    try:
        # Extraer el ID del curso del enlace de checkout
        course_id_match = re.search(r'/course/(\d+)/', checkout_url)
        if course_id_match:
            course_id = course_id_match.group(1)
            # Construir el enlace directo del curso
            course_url = f"https://www.udemy.com/course/{course_id}/"
            return course_url
        return checkout_url
    except:
        return checkout_url

def extract_coupon_code_from_url(url):
    """Extraer código de cupón de la URL"""
    try:
        # Buscar discountCode en la URL
        discount_match = re.search(r'discountCode=([A-Z0-9]+)', url)
        if discount_match:
            return discount_match.group(1)
        
        # Buscar couponCode en la URL
        coupon_match = re.search(r'couponCode=([A-Z0-9]+)', url)
        if coupon_match:
            return coupon_match.group(1)
        
        return None
    except:
        return None

def verify_course_is_free(driver, udemy_url):
    """Verificar si el curso es 100% gratis navegando a la página de Udemy"""
    try:
        print(f"🔍 Verificando si el curso es gratis: {udemy_url}")
        
        # Navegar a la página del curso
        driver.get(udemy_url)
        time.sleep(3)
        
        # Obtener el texto de la página
        page_text = driver.page_source.lower()
        
        # Buscar indicadores específicos de precio (más precisos)
        price_patterns = [
            r'\$\d+\.?\d*',  # $19.99, $20, etc.
            r'€\d+\.?\d*',   # €19.99, €20, etc.
            r'£\d+\.?\d*',   # £19.99, £20, etc.
            r'\d+\.?\d*\s*\$',  # 19.99 $, 20 $, etc.
            r'\d+\.?\d*\s*€',   # 19.99 €, 20 €, etc.
            r'\d+\.?\d*\s*£',   # 19.99 £, 20 £, etc.
            r'precio.*?\$\d+',  # precio $19
            r'price.*?\$\d+',   # price $19
            r'costo.*?\$\d+',   # costo $19
            r'cost.*?\$\d+'     # cost $19
        ]
        
        # Verificar si hay precios específicos (no $0)
        has_price = False
        for pattern in price_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            for match in matches:
                # Extraer solo el número del precio
                price_number = re.search(r'\d+\.?\d*', match)
                if price_number:
                    price_value = float(price_number.group())
                    if price_value > 0:  # Si el precio es mayor a 0
                        has_price = True
                        print(f"❌ Precio detectado: {match} (valor: {price_value})")
                        break
            if has_price:
                break
        
        # Buscar indicadores específicos de gratis (más amplios)
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
            "add to cart",
            "agregar al carrito",
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
        
        # Buscar botones específicos de inscripción gratuita (más selectores)
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
        
        # Buscar elementos con precio $0 o 0€
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
        
        # Lógica de decisión mejorada
        if has_price and not is_free:
            print("❌ El curso tiene precio, no es gratis")
            return False
        elif is_free:
            print("✅ El curso es 100% gratis")
            return True
        else:
            # Verificación adicional: buscar si hay botones de compra
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
            
            # Si no encontramos indicadores claros, ser más permisivo
            print("⚠️ No se encontraron indicadores claros, verificando cupón...")
            
            # Verificar si el cupón hace el curso gratis
            if 'couponcode=' in udemy_url.lower():
                print("✅ Cupón detectado en URL, asumiendo que puede hacer el curso gratis")
                return True
            
            print("❌ No se encontraron indicadores claros de que sea gratis")
            return False
        
    except Exception as e:
        print(f"⚠️ Error verificando si el curso es gratis: {e}")
        return False

def extraer_cursos_de_coupon_scorpion(driver):
    """Extraer cursos directamente de Coupon Scorpion"""
    print("🔍 Extrayendo cursos de Coupon Scorpion...")
    
    udemy_links = []
    processed_courses = set()
    
    try:
        # Navegar a la página específica de 100% Off Coupons
        print("🌐 Navegando a la página de 100% Off Coupons...")
        driver.set_page_load_timeout(30)
        driver.get("https://couponscorpion-com.translate.goog/category/100-off-coupons/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc")
        time.sleep(3)
        
        # Verificar que la página cargó correctamente
        if "100-off-coupons" not in driver.current_url.lower():
            print("❌ Error: No se pudo cargar la página de 100% Off Coupons")
            return udemy_links
        
        print("✅ Página cargada correctamente")
        
        # Hacer scroll para cargar más cursos
        print("📜 Haciendo scroll para cargar cursos...")
        for scroll in range(3):  # Reducir a 3 scrolls
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                print(f"Scroll {scroll+1}/3 completado")
            except Exception as e:
                print(f"⚠️ Error en scroll {scroll+1}: {e}")
                break
        
        # Buscar enlaces de cursos en la página principal
        print("🔍 Buscando enlaces de cursos en la página...")
        
        try:
            # Buscar enlaces en títulos
            course_links = driver.find_elements(By.XPATH, "//h2//a")
            if not course_links:
                course_links = driver.find_elements(By.XPATH, "//h3//a")
            
            # Eliminar duplicados y guardar URLs
            unique_urls = []
            seen_urls = set()
            for link in course_links:
                try:
                    href = link.get_attribute("href")
                    if href and href not in seen_urls and "couponscorpion" in href:
                        seen_urls.add(href)
                        unique_urls.append(href)
                except:
                    continue
            
            course_urls = unique_urls
            print(f"🔍 Encontrados {len(course_urls)} enlaces únicos de cursos...")
            
            # Mostrar algunos enlaces para debug
            for i, url in enumerate(course_urls[:3]):
                print(f"📄 Enlace {i+1}: {url}")
                
        except Exception as e:
            print(f"❌ Error buscando enlaces: {e}")
            return udemy_links
        
        # Procesar solo los primeros 10 enlaces para la prueba
        for i in range(min(10, len(course_urls))):
            try:
                print(f"🔍 Procesando enlace {i+1}/10...")
                
                if i >= len(course_urls):
                    print("⚠️ No hay más enlaces disponibles")
                    break
                
                link_url = course_urls[i]
                print(f"📄 URL del enlace: {link_url}")
                
                # Inicializar variables para este curso
                coupon_code = None
                udemy_url = None
                original_url = None
                
                # Navegar directamente a la página del curso
                try:
                    driver.get(link_url)
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Error navegando a la página: {e}")
                    continue
                
                # Buscar el botón "OBTENER CÓDIGO DE CUPÓN" o "GET COUPON CODE"
                print("🔍 Buscando botón de obtener cupón...")
                coupon_button_selectors = [
                    "//button[contains(text(), 'OBTENER CÓDIGO DE CUPÓN')]",
                    "//button[contains(text(), 'GET COUPON CODE')]",
                    "//a[contains(text(), 'OBTENER CÓDIGO DE CUPÓN')]",
                    "//a[contains(text(), 'GET COUPON CODE')]",
                    "//button[contains(text(), 'cupón') or contains(text(), 'coupon')]",
                    "//a[contains(text(), 'cupón') or contains(text(), 'coupon')]",
                    "//*[contains(text(), 'OBTENER') and contains(text(), 'CUPÓN')]",
                    "//*[contains(text(), 'GET') and contains(text(), 'COUPON')]"
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
                    # Verificar si el botón tiene un enlace
                    button_href = coupon_button.get_attribute("href")
                    print(f"🔗 Href del botón: {button_href}")
                    
                    # Si el botón tiene un enlace de redirección, seguirlo
                    if button_href and ("out.php" in button_href or "redirect" in button_href):
                        print("🔍 Encontrado enlace de redirección, siguiéndolo...")
                        try:
                            driver.get(button_href)
                            time.sleep(3)
                            
                            # Verificar si se redirigió a Udemy
                            current_url = driver.current_url
                            print(f"🔍 URL después de la redirección: {current_url}")
                            
                            if "udemy.com/course/" in current_url:
                                print("✅ ¡Enlace de Udemy encontrado después de la redirección!")
                                udemy_url = current_url
                                original_url = current_url  # Guardar la URL original
                                
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
                            else:
                                # SIEMPRE buscar botón "INSCRIBIRSE" o "ENROLL" para obtener el enlace final
                                print("🔍 Buscando botón INSCRIBIRSE/ENROLL para obtener el enlace final...")
                                enroll_button_selectors = [
                                    "//button[contains(text(), 'INSCRIBIRSE')]",
                                    "//button[contains(text(), 'ENROLL')]",
                                    "//a[contains(text(), 'INSCRIBIRSE')]",
                                    "//a[contains(text(), 'ENROLL')]",
                                    "//*[contains(text(), 'INSCRIBIRSE')]",
                                    "//*[contains(text(), 'ENROLL')]",
                                    "//button[contains(text(), 'inscribirse')]",
                                    "//button[contains(text(), 'enroll')]",
                                    "//a[contains(text(), 'inscribirse')]",
                                    "//a[contains(text(), 'enroll')]"
                                ]
                                
                                enroll_button = None
                                for selector in enroll_button_selectors:
                                    try:
                                        buttons = driver.find_elements(By.XPATH, selector)
                                        if buttons:
                                            enroll_button = buttons[0]
                                            print(f"✅ Botón INSCRIBIRSE encontrado con selector: {selector}")
                                            break
                                    except Exception as e:
                                        continue
                                
                                if enroll_button:
                                    try:
                                        print("🖱️ Haciendo clic en botón INSCRIBIRSE para obtener el enlace final...")
                                        enroll_button.click()
                                        time.sleep(3)
                                        
                                        # Verificar si ahora estamos en Udemy
                                        current_url = driver.current_url
                                        print(f"🔍 URL después de hacer clic en INSCRIBIRSE: {current_url}")
                                        
                                        if "udemy.com/course/" in current_url:
                                            print("✅ ¡Enlace de Udemy encontrado después de hacer clic en INSCRIBIRSE!")
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
                                        else:
                                            print("⚠️ No se llegó a Udemy después de hacer clic en INSCRIBIRSE")
                                            continue
                                    except Exception as e:
                                        print(f"⚠️ Error haciendo clic en INSCRIBIRSE: {e}")
                                        continue
                                else:
                                    print("⚠️ No se encontró botón INSCRIBIRSE")
                                    continue
                            
                            # Procesar el curso si tenemos cupón y URL de Udemy
                            if coupon_code and udemy_url:
                                print(f"🎫 Código de cupón encontrado: {coupon_code}")
                                
                                # Extraer ID del curso para evitar duplicados
                                course_id = extract_course_id(udemy_url)
                                
                                if course_id not in processed_courses:
                                    # SIEMPRE verificar si el curso es realmente gratis navegando a la página final
                                    print("🔍 Verificando si el curso es 100% gratis navegando a la página final...")
                                    is_free = verify_course_is_free(driver, udemy_url)
                                    
                                    if is_free:
                                        processed_courses.add(course_id)
                                        
                                        # Construir URL completa con cupón
                                        # Verificar si la URL ya tiene couponCode
                                        if "couponCode=" in udemy_url:
                                            full_url = udemy_url
                                        else:
                                            full_url = f"{udemy_url}?couponCode={coupon_code}"
                                        
                                        udemy_links.append({
                                            'text': f"Curso de Coupon Scorpion: {extract_course_name(udemy_url)}",
                                            'urls': [full_url],
                                            'index': len(udemy_links),
                                            'screenshot': None
                                        })
                                        print(f"✅ Curso GRATIS agregado: {extract_course_name(udemy_url)}")
                                        print(f"🎫 Código del cupón: {coupon_code}")
                                        print(f"🔗 URL completa: {full_url}")
                                    else:
                                        print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                                else:
                                    print(f"⚠️ Curso duplicado ignorado: {course_id}")
                            else:
                                print("❌ No se encontró código de cupón o URL de Udemy válida")
                            
                            # Volver a la página anterior
                            driver.back()
                            time.sleep(2)
                            continue
                        except Exception as e:
                            print(f"⚠️ Error siguiendo la redirección: {e}")
                            try:
                                driver.back()
                                time.sleep(2)
                            except:
                                pass
                    else:
                        # Si el botón no tiene href, hacer clic directamente en él
                        print("🖱️ El botón no tiene href, haciendo clic directamente...")
                        try:
                            coupon_button.click()
                            time.sleep(3)
                            
                            # Verificar si se redirigió a Udemy
                            current_url = driver.current_url
                            print(f"🔍 URL después de hacer clic en el botón: {current_url}")
                            
                            if "udemy.com/course/" in current_url:
                                print("✅ ¡Enlace de Udemy encontrado después de hacer clic en el botón!")
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
                                        # SIEMPRE verificar si el curso es realmente gratis navegando a la página final
                                        print("🔍 Verificando si el curso es 100% gratis navegando a la página final...")
                                        is_free = verify_course_is_free(driver, udemy_url)
                                        
                                        if is_free:
                                            processed_courses.add(course_id)
                                            
                                            # Construir URL completa con cupón
                                            # Verificar si la URL ya tiene couponCode
                                            if "couponCode=" in udemy_url:
                                                full_url = udemy_url
                                            else:
                                                full_url = f"{udemy_url}?couponCode={coupon_code}"
                                            
                                            udemy_links.append({
                                                'text': f"Curso de Coupon Scorpion: {extract_course_name(udemy_url)}",
                                                'urls': [full_url],
                                                'index': len(udemy_links),
                                                'screenshot': None
                                            })
                                            print(f"✅ Curso GRATIS agregado: {extract_course_name(udemy_url)}")
                                            print(f"🎫 Código del cupón: {coupon_code}")
                                            print(f"🔗 URL completa: {full_url}")
                                        else:
                                            print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                                    else:
                                        print(f"⚠️ Curso duplicado ignorado: {course_id}")
                                else:
                                    print("❌ No se encontró código de cupón o URL de Udemy válida")
                            else:
                                # Si no es Udemy, buscar botón "INSCRIBIRSE" o "ENROLL"
                                print("🔍 Buscando botón INSCRIBIRSE/ENROLL para obtener el enlace final...")
                                enroll_button_selectors = [
                                    "//button[contains(text(), 'INSCRIBIRSE')]",
                                    "//button[contains(text(), 'ENROLL')]",
                                    "//a[contains(text(), 'INSCRIBIRSE')]",
                                    "//a[contains(text(), 'ENROLL')]",
                                    "//*[contains(text(), 'INSCRIBIRSE')]",
                                    "//*[contains(text(), 'ENROLL')]",
                                    "//button[contains(text(), 'inscribirse')]",
                                    "//button[contains(text(), 'enroll')]",
                                    "//a[contains(text(), 'inscribirse')]",
                                    "//a[contains(text(), 'enroll')]"
                                ]
                                
                                enroll_button = None
                                for selector in enroll_button_selectors:
                                    try:
                                        buttons = driver.find_elements(By.XPATH, selector)
                                        if buttons:
                                            enroll_button = buttons[0]
                                            print(f"✅ Botón INSCRIBIRSE encontrado con selector: {selector}")
                                            break
                                    except Exception as e:
                                        continue
                                
                                if enroll_button:
                                    try:
                                        print("🖱️ Haciendo clic en botón INSCRIBIRSE para obtener el enlace final...")
                                        enroll_button.click()
                                        time.sleep(3)
                                        
                                        # Verificar si ahora estamos en Udemy
                                        current_url = driver.current_url
                                        print(f"🔍 URL después de hacer clic en INSCRIBIRSE: {current_url}")
                                        
                                        if "udemy.com/course/" in current_url:
                                            print("✅ ¡Enlace de Udemy encontrado después de hacer clic en INSCRIBIRSE!")
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
                                                    # SIEMPRE verificar si el curso es realmente gratis navegando a la página final
                                                    print("🔍 Verificando si el curso es 100% gratis navegando a la página final...")
                                                    is_free = verify_course_is_free(driver, udemy_url)
                                                    
                                                    if is_free:
                                                        processed_courses.add(course_id)
                                                        
                                                        # Construir URL completa con cupón
                                                        # Verificar si la URL ya tiene couponCode
                                                        if "couponCode=" in udemy_url:
                                                            full_url = udemy_url
                                                        else:
                                                            full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                        
                                                        udemy_links.append({
                                                            'text': f"Curso de Coupon Scorpion: {extract_course_name(udemy_url)}",
                                                            'urls': [full_url],
                                                            'index': len(udemy_links),
                                                            'screenshot': None
                                                        })
                                                        print(f"✅ Curso GRATIS agregado: {extract_course_name(udemy_url)}")
                                                        print(f"🎫 Código del cupón: {coupon_code}")
                                                        print(f"🔗 URL completa: {full_url}")
                                                    else:
                                                        print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                                                else:
                                                    print(f"⚠️ Curso duplicado ignorado: {course_id}")
                                            else:
                                                print("❌ No se encontró código de cupón o URL de Udemy válida")
                                        else:
                                            print("⚠️ No se llegó a Udemy después de hacer clic en INSCRIBIRSE")
                                            continue
                                    except Exception as e:
                                        print(f"⚠️ Error haciendo clic en INSCRIBIRSE: {e}")
                                        continue
                                else:
                                    print("⚠️ No se encontró botón INSCRIBIRSE")
                                    continue
                            
                            # Volver a la página anterior
                            driver.back()
                            time.sleep(2)
                            continue
                        except Exception as e:
                            print(f"⚠️ Error haciendo clic en el botón: {e}")
                            try:
                                driver.back()
                                time.sleep(2)
                            except:
                                pass
                            continue
                else:
                    print("⚠️ No se encontró el botón de obtener cupón")
                
                # Volver a la página principal
                try:
                    driver.back()
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Error volviendo atrás: {e}")
                    driver.get("https://couponscorpion-com.translate.goog/category/100-off-coupons/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc")
                    time.sleep(3)
                
            except Exception as e:
                print(f"⚠️ Error procesando curso {i+1}: {e}")
                try:
                    driver.back()
                    time.sleep(2)
                except:
                    driver.get("https://couponscorpion-com.translate.goog/category/100-off-coupons/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc")
                    time.sleep(3)
                continue
    
    except Exception as e:
        print(f"❌ Error en extraer_cursos_de_coupon_scorpion: {e}")
    
    print(f"📊 Cursos extraídos de Coupon Scorpion: {len(udemy_links)}")
    return udemy_links

def extraer_cursos_de_cursosdev_categoria(driver, categoria_url, max_cursos=10, processed_courses=None):
    """Extraer cursos de una categoría específica de CursosDev"""
    print(f"🔍 Extrayendo cursos de categoría: {categoria_url}")
    
    udemy_links = []
    if processed_courses is None:
        processed_courses = set()
    
    try:
        # Navegar a la página de la categoría específica
        print(f"🌐 Navegando a la categoría: {categoria_url}")
        driver.set_page_load_timeout(30)
        driver.get(categoria_url)
        time.sleep(3)
        
        # Verificar que la página cargó correctamente
        if "cursosdev.com" not in driver.current_url.lower():
            print("❌ Error: No se pudo cargar la página de la categoría")
            return udemy_links, processed_courses
        
        print("✅ Página de categoría cargada correctamente")
        
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
        
        # Buscar enlaces de cursos en la página
        print("🔍 Buscando enlaces de cursos en la categoría...")
        
        try:
            # Buscar TODOS los enlaces en la página para debug
            all_links = driver.find_elements(By.XPATH, "//a[@href]")
            print(f"🔍 Total de enlaces encontrados en la página: {len(all_links)}")
            
            # Mostrar algunos enlaces para debug
            for i, link in enumerate(all_links[:10]):
                try:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    print(f"📄 Enlace {i+1}: {href} - Texto: {text[:50]}")
                except:
                    continue
            
            # Buscar enlaces específicos de cursos
            course_links = []
            
            # Buscar enlaces que contengan "udemy"
            udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'udemy.com')]")
            course_links.extend(udemy_links)
            print(f"🔍 Enlaces de Udemy encontrados: {len(udemy_links)}")
            
            # Buscar enlaces que contengan "coupons-udemy" en la URL (formato específico de CursosDev)
            coupons_udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'coupons-udemy')]")
            course_links.extend(coupons_udemy_links)
            print(f"🔍 Enlaces con 'coupons-udemy' encontrados: {len(coupons_udemy_links)}")
            
            # Buscar enlaces en títulos de cursos (pero excluir categorías)
            title_links = driver.find_elements(By.XPATH, "//h1//a | //h2//a | //h3//a | //h4//a | //h5//a")
            course_links.extend(title_links)
            print(f"🔍 Enlaces en títulos encontrados: {len(title_links)}")
            
            # Buscar enlaces en artículos o cards de cursos
            article_links = driver.find_elements(By.XPATH, "//article//a | //div[contains(@class, 'card')]//a | //div[contains(@class, 'post')]//a | //div[contains(@class, 'course')]//a | //div[contains(@class, 'entry')]//a")
            course_links.extend(article_links)
            print(f"🔍 Enlaces en artículos/cards encontrados: {len(article_links)}")
            
            # Buscar enlaces que contengan palabras clave de cursos
            keyword_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'curso') or contains(text(), 'course') or contains(text(), 'udemy') or contains(text(), 'cupón') or contains(text(), 'coupon')]")
            course_links.extend(keyword_links)
            print(f"🔍 Enlaces con palabras clave encontrados: {len(keyword_links)}")
            
            # Buscar enlaces que contengan "cupón" o "coupon"
            coupon_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'cupón') or contains(text(), 'coupon')]")
            course_links.extend(coupon_links)
            print(f"🔍 Enlaces con 'cupón' encontrados: {len(coupon_links)}")
            
            # Buscar enlaces que contengan "obtener" o "get"
            obtener_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'obtener') or contains(text(), 'get')]")
            course_links.extend(obtener_links)
            print(f"🔍 Enlaces con 'obtener/get' encontrados: {len(obtener_links)}")
            
            # Buscar enlaces en listas de cursos
            list_links = driver.find_elements(By.XPATH, "//ul//a | //ol//a | //li//a")
            course_links.extend(list_links)
            print(f"🔍 Enlaces en listas encontrados: {len(list_links)}")
            
            # Procesar los enlaces encontrados
            all_course_urls = []
            seen_urls = set()
            for link in course_links:
                try:
                    href = link.get_attribute("href")
                    if href and href not in seen_urls and href.startswith('http'):
                        # Filtrar solo URLs que parezcan ser de cursos individuales (no categorías)
                        if (('cursosdev.com' in href and ('coupons-udemy' in href or 'udemy.com' in href)) or
                            'udemy.com' in href or
                            # Excluir URLs de categorías como /courses/JavaScript, /courses/Angular, etc.
                            (href.startswith('https://cursosdev.com/') and 
                             not href.startswith('https://cursosdev.com/courses/') and
                             not href.startswith('https://cursosdev.com/blog') and
                             not href.startswith('https://cursosdev.com/submit'))):
                            seen_urls.add(href)
                            all_course_urls.append(href)
                except:
                    continue
            
            # Si no encontramos cursos específicos, buscar enlaces que no sean categorías
            if not all_course_urls:
                # Eliminar duplicados y guardar URLs
                unique_urls = []
                for link in course_links:
                    try:
                        href = link.get_attribute("href")
                        if href and href not in seen_urls and href.startswith('http'):
                            # Incluir cualquier enlace de cursosdev que no sea una categoría
                            if (href.startswith('https://cursosdev.com/') and 
                                not href.startswith('https://cursosdev.com/courses/') and
                                not href.startswith('https://cursosdev.com/blog') and
                                not href.startswith('https://cursosdev.com/submit')):
                                seen_urls.add(href)
                                unique_urls.append(href)
                    except:
                        continue
                
                all_course_urls = unique_urls
            
            course_urls = all_course_urls
            print(f"🔍 Encontrados {len(course_urls)} enlaces únicos de cursos en la categoría...")
            
            # Mostrar algunos enlaces para debug
            for i, url in enumerate(course_urls[:5]):
                print(f"📄 Enlace de curso {i+1}: {url}")
                
        except Exception as e:
            print(f"❌ Error buscando enlaces en la categoría: {e}")
            return udemy_links, processed_courses
        
        # Procesar enlaces hasta encontrar max_cursos válidos
        valid_courses_found = 0
        for i in range(len(course_urls)):
            # Limitar a procesar máximo max_cursos válidos - verificar ANTES de procesar
            if valid_courses_found >= max_cursos:
                print(f"✅ Ya se encontraron {max_cursos} cursos válidos en la categoría, deteniendo búsqueda")
                break
                
            try:
                print(f"🔍 Procesando enlace {i+1}/{len(course_urls)} de la categoría...")
                
                if i >= len(course_urls):
                    print("⚠️ No hay más enlaces disponibles en la categoría")
                    break
                
                link_url = course_urls[i]
                print(f"📄 URL del enlace: {link_url}")
                
                # Inicializar variables para este curso
                coupon_code = None
                udemy_url = None
                original_url = None
                
                # Navegar directamente a la página del curso
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
                                
                                # Construir URL completa con cupón
                                if "couponCode=" in udemy_url:
                                    full_url = udemy_url
                                else:
                                    full_url = f"{udemy_url}?couponCode={coupon_code}"
                                
                                udemy_links.append({
                                    'text': f"Curso de CursosDev (IT & Software): {extract_course_name(udemy_url)}",
                                    'urls': [full_url],
                                    'index': len(udemy_links),
                                    'screenshot': None
                                })
                                valid_courses_found += 1
                                print(f"✅ Curso GRATIS de categoría agregado: {extract_course_name(udemy_url)}")
                                print(f"🎫 Código del cupón: {coupon_code}")
                                print(f"🔗 URL completa: {full_url}")
                                print(f"📊 Cursos válidos encontrados en categoría: {valid_courses_found}/{max_cursos}")
                            else:
                                print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                        else:
                            print(f"⚠️ Curso duplicado ignorado: {course_id}")
                    else:
                        print("❌ No se encontró código de cupón o URL de Udemy válida")
                else:
                    # Buscar botón "OBTENER CUPÓN" o similar en CursosDev
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
                        # Agregar selectores para el formato con emoji
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
                                                    
                                                    # Construir URL completa con cupón
                                                    if "couponCode=" in udemy_url:
                                                        full_url = udemy_url
                                                    else:
                                                        full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                    
                                                    udemy_links.append({
                                                        'text': f"Curso de CursosDev (IT & Software): {extract_course_name(udemy_url)}",
                                                        'urls': [full_url],
                                                        'index': len(udemy_links),
                                                        'screenshot': None
                                                    })
                                                    valid_courses_found += 1
                                                    print(f"✅ Curso GRATIS de categoría agregado: {extract_course_name(udemy_url)}")
                                                    print(f"🎫 Código del cupón: {coupon_code}")
                                                    print(f"🔗 URL completa: {full_url}")
                                                    print(f"📊 Cursos válidos encontrados en categoría: {valid_courses_found}/{max_cursos}")
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
                                                
                                                # Construir URL completa con cupón
                                                if "couponCode=" in udemy_url:
                                                    full_url = udemy_url
                                                else:
                                                    full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                
                                                udemy_links.append({
                                                    'text': f"Curso de CursosDev (IT & Software): {extract_course_name(udemy_url)}",
                                                    'urls': [full_url],
                                                    'index': len(udemy_links),
                                                    'screenshot': None
                                                })
                                                valid_courses_found += 1
                                                print(f"✅ Curso GRATIS de categoría agregado: {extract_course_name(udemy_url)}")
                                                print(f"🎫 Código del cupón: {coupon_code}")
                                                print(f"🔗 URL completa: {full_url}")
                                                print(f"📊 Cursos válidos encontrados en categoría: {valid_courses_found}/{max_cursos}")
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
                
                # Volver a la página de la categoría
                try:
                    driver.back()
                    time.sleep(2)
                except Exception as e:
                    print(f"⚠️ Error volviendo atrás: {e}")
                    driver.get(categoria_url)
                    time.sleep(3)
                
            except Exception as e:
                print(f"⚠️ Error procesando curso {i+1} de la categoría: {e}")
                try:
                    driver.back()
                    time.sleep(2)
                except:
                    driver.get(categoria_url)
                    time.sleep(3)
                continue
    
    except Exception as e:
        print(f"❌ Error en extraer_cursos_de_cursosdev_categoria: {e}")
    
    print(f"📊 Cursos extraídos de la categoría: {len(udemy_links)}")
    return udemy_links, processed_courses

def extraer_cursos_de_cursosdev(driver, processed_courses=None, max_cursos=10):
    """Extraer cursos directamente de CursosDev"""
    print("🔍 Extrayendo cursos de CursosDev...")
    
    udemy_links = []
    if processed_courses is None:
        processed_courses = set()
    
    try:
        # Navegar directamente a la página principal de CursosDev
        print("🌐 Navegando a la página principal de CursosDev...")
        driver.set_page_load_timeout(30)
        driver.get("https://cursosdev.com/")
        time.sleep(3)
        
        # Verificar que la página cargó correctamente
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
        
        # Buscar enlaces de cursos en la página
        print("🔍 Buscando enlaces de cursos en CursosDev...")
        
        try:
            # Buscar TODOS los enlaces en la página para debug
            all_links = driver.find_elements(By.XPATH, "//a[@href]")
            print(f"🔍 Total de enlaces encontrados en la página: {len(all_links)}")
            
            # Mostrar algunos enlaces para debug
            for i, link in enumerate(all_links[:10]):
                try:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    print(f"📄 Enlace {i+1}: {href} - Texto: {text[:50]}")
                except:
                    continue
            
            # Buscar enlaces específicos de cursos
            course_links = []
            
            # Buscar enlaces específicos de cursos en la página actual
            course_links = []
            
            # Buscar enlaces que contengan "udemy"
            udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'udemy.com')]")
            course_links.extend(udemy_links)
            print(f"🔍 Enlaces de Udemy encontrados: {len(udemy_links)}")
            
            # Buscar enlaces que contengan "coupons-udemy" en la URL (formato específico de CursosDev)
            coupons_udemy_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'coupons-udemy')]")
            course_links.extend(coupons_udemy_links)
            print(f"🔍 Enlaces con 'coupons-udemy' encontrados: {len(coupons_udemy_links)}")
            
            # Buscar enlaces en títulos de cursos (pero excluir categorías)
            title_links = driver.find_elements(By.XPATH, "//h1//a | //h2//a | //h3//a | //h4//a | //h5//a")
            course_links.extend(title_links)
            print(f"🔍 Enlaces en títulos encontrados: {len(title_links)}")
            
            # Buscar enlaces en artículos o cards de cursos
            article_links = driver.find_elements(By.XPATH, "//article//a | //div[contains(@class, 'card')]//a | //div[contains(@class, 'post')]//a | //div[contains(@class, 'course')]//a | //div[contains(@class, 'entry')]//a")
            course_links.extend(article_links)
            print(f"🔍 Enlaces en artículos/cards encontrados: {len(article_links)}")
            
            # Buscar enlaces que contengan palabras clave de cursos
            keyword_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'curso') or contains(text(), 'course') or contains(text(), 'udemy') or contains(text(), 'cupón') or contains(text(), 'coupon')]")
            course_links.extend(keyword_links)
            print(f"🔍 Enlaces con palabras clave encontrados: {len(keyword_links)}")
            
            # Buscar enlaces que contengan "cupón" o "coupon"
            coupon_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'cupón') or contains(text(), 'coupon')]")
            course_links.extend(coupon_links)
            print(f"🔍 Enlaces con 'cupón' encontrados: {len(coupon_links)}")
            
            # Buscar enlaces que contengan "obtener" o "get"
            obtener_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'obtener') or contains(text(), 'get')]")
            course_links.extend(obtener_links)
            print(f"🔍 Enlaces con 'obtener/get' encontrados: {len(obtener_links)}")
            
            # Buscar enlaces en listas de cursos
            list_links = driver.find_elements(By.XPATH, "//ul//a | //ol//a | //li//a")
            course_links.extend(list_links)
            print(f"🔍 Enlaces en listas encontrados: {len(list_links)}")
            
            # Procesar los enlaces encontrados
            all_course_urls = []
            seen_urls = set()
            for link in course_links:
                try:
                    href = link.get_attribute("href")
                    if href and href not in seen_urls and href.startswith('http'):
                        # Filtrar solo URLs que parezcan ser de cursos individuales (no categorías)
                        if (('cursosdev.com' in href and ('coupons-udemy' in href or 'udemy.com' in href)) or
                            'udemy.com' in href or
                            # Excluir URLs de categorías como /courses/JavaScript, /courses/Angular, etc.
                            (href.startswith('https://cursosdev.com/') and 
                             not href.startswith('https://cursosdev.com/courses/') and
                             not href.startswith('https://cursosdev.com/blog') and
                             not href.startswith('https://cursosdev.com/submit'))):
                            seen_urls.add(href)
                            all_course_urls.append(href)
                except:
                    continue
            
            # Si no encontramos cursos específicos, buscar enlaces que no sean categorías
            if not all_course_urls:
                # Eliminar duplicados y guardar URLs
                unique_urls = []
                for link in course_links:
                    try:
                        href = link.get_attribute("href")
                        if href and href not in seen_urls and href.startswith('http'):
                            # Incluir cualquier enlace de cursosdev que no sea una categoría
                            if (href.startswith('https://cursosdev.com/') and 
                                not href.startswith('https://cursosdev.com/courses/') and
                                not href.startswith('https://cursosdev.com/blog') and
                                not href.startswith('https://cursosdev.com/submit')):
                                seen_urls.add(href)
                                unique_urls.append(href)
                    except:
                        continue
                
                all_course_urls = unique_urls
            
            course_urls = all_course_urls
            print(f"🔍 Encontrados {len(course_urls)} enlaces únicos de cursos en CursosDev...")
            
            # Mostrar algunos enlaces para debug
            for i, url in enumerate(course_urls[:5]):
                print(f"📄 Enlace de curso {i+1}: {url}")
                
        except Exception as e:
            print(f"❌ Error buscando enlaces en CursosDev: {e}")
            return udemy_links
        
        # Procesar enlaces hasta encontrar 10 cursos válidos
        valid_courses_found = 0
        for i in range(len(course_urls)):
            # Limitar a procesar máximo 10 cursos válidos - verificar ANTES de procesar
            if valid_courses_found >= 10:
                print(f"✅ Ya se encontraron 10 cursos válidos, deteniendo búsqueda")
                break
                
            try:
                print(f"🔍 Procesando enlace {i+1}/{len(course_urls)} de CursosDev...")
                
                if i >= len(course_urls):
                    print("⚠️ No hay más enlaces disponibles en CursosDev")
                    break
                
                link_url = course_urls[i]
                print(f"📄 URL del enlace: {link_url}")
                
                # Inicializar variables para este curso
                coupon_code = None
                udemy_url = None
                original_url = None
                
                # Navegar directamente a la página del curso
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
                                
                                # Construir URL completa con cupón
                                if "couponCode=" in udemy_url:
                                    full_url = udemy_url
                                else:
                                    full_url = f"{udemy_url}?couponCode={coupon_code}"
                                
                                udemy_links.append({
                                    'text': f"Curso de CursosDev: {extract_course_name(udemy_url)}",
                                    'urls': [full_url],
                                    'index': len(udemy_links),
                                    'screenshot': None
                                })
                                valid_courses_found += 1
                                print(f"✅ Curso GRATIS de CursosDev agregado: {extract_course_name(udemy_url)}")
                                print(f"🎫 Código del cupón: {coupon_code}")
                                print(f"🔗 URL completa: {full_url}")
                                print(f"📊 Cursos válidos encontrados: {valid_courses_found}/10")
                            else:
                                print(f"❌ Curso descartado - tiene precio: {extract_course_name(udemy_url)}")
                        else:
                            print(f"⚠️ Curso duplicado ignorado: {course_id}")
                    else:
                        print("❌ No se encontró código de cupón o URL de Udemy válida")
                else:
                    # Buscar botón "OBTENER CUPÓN" o similar en CursosDev
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
                        # Agregar selectores para el formato con emoji
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
                                                    
                                                    # Construir URL completa con cupón
                                                    if "couponCode=" in udemy_url:
                                                        full_url = udemy_url
                                                    else:
                                                        full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                    
                                                    udemy_links.append({
                                                        'text': f"Curso de CursosDev: {extract_course_name(udemy_url)}",
                                                        'urls': [full_url],
                                                        'index': len(udemy_links),
                                                        'screenshot': None
                                                    })
                                                    valid_courses_found += 1
                                                    print(f"✅ Curso GRATIS de CursosDev agregado: {extract_course_name(udemy_url)}")
                                                    print(f"🎫 Código del cupón: {coupon_code}")
                                                    print(f"🔗 URL completa: {full_url}")
                                                    print(f"📊 Cursos válidos encontrados: {valid_courses_found}/10")
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
                                                
                                                # Construir URL completa con cupón
                                                if "couponCode=" in udemy_url:
                                                    full_url = udemy_url
                                                else:
                                                    full_url = f"{udemy_url}?couponCode={coupon_code}"
                                                
                                                udemy_links.append({
                                                    'text': f"Curso de CursosDev: {extract_course_name(udemy_url)}",
                                                    'urls': [full_url],
                                                    'index': len(udemy_links),
                                                    'screenshot': None
                                                })
                                                valid_courses_found += 1
                                                print(f"✅ Curso GRATIS de CursosDev agregado: {extract_course_name(udemy_url)}")
                                                print(f"🎫 Código del cupón: {coupon_code}")
                                                print(f"🔗 URL completa: {full_url}")
                                                print(f"📊 Cursos válidos encontrados: {valid_courses_found}/10")
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
                print(f"⚠️ Error procesando curso {i+1} de CursosDev: {e}")
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
    return udemy_links, processed_courses

def run_bot_envio_directo():
    """Bot principal que extrae cursos CON CUPONES de CursosDev y los envía por WhatsApp"""
    print("🚀 Iniciando bot de extracción de cursos CON CUPONES...")
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🎯 BOT DE EXTRACCIÓN - CURSOS CON CUPONES")
    print("=" * 60)
    print("Extrae cursos de Udemy con cupones de CursosDev")
    print("Los envía directamente por WhatsApp")
    print("=" * 60)
    
    driver = None
    
    try:
        # 1. INICIALIZAR DRIVER DE CHROME
        print("\nPASO 1: Inicializando navegador...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # 2. EXTRAER CURSOS DE CURSOSDEV (CATEGORÍA IT & SOFTWARE PRIMERO)
        print("\nPASO 2: Extrayendo cursos CON CUPONES de CursosDev...")
        all_courses = []
        processed_courses = set()  # Para evitar duplicados entre fuentes
        
                # Primero extraer 10 cursos de la categoría IT & Software
        print("🌐 Extrayendo de CursosDev - Categoría IT & Software...")
        categoria_url = "https://cursosdev.com/category/it-and-software/1"
        posts_categoria, processed_courses = extraer_cursos_de_cursosdev_categoria(driver, categoria_url, max_cursos=10, processed_courses=processed_courses)
        
        # Luego extraer cursos de la página principal de CursosDev
        print("🌐 Extrayendo de CursosDev - Página principal...")
        posts_cursosdev, processed_courses = extraer_cursos_de_cursosdev(driver, processed_courses, max_cursos=10)
        
        # Combinar ambos resultados
        all_posts = posts_categoria + posts_cursosdev
        
        # Procesar directamente los cursos extraídos
        print(f"Total de cursos extraídos de categoría IT & Software: {len(posts_categoria)}")
        print(f"Total de cursos extraídos de página principal: {len(posts_cursosdev)}")
        print(f"Total combinado: {len(all_posts)}")
        
        # Verificar que se extrajeron cursos correctamente
        if not all_posts:
            print("❌ No se extrajeron cursos de CursosDev")
            return False
        
        # Procesar los cursos extraídos con URLs de Udemy y cupones
        print(f"Procesando {len(all_posts)} cursos extraídos...")
        
        for i, post in enumerate(all_posts):
            try:
                # Verificar que el post tenga la estructura correcta
                if isinstance(post, dict) and 'urls' in post and post['urls']:
                    udemy_url = post['urls'][0]  # La URL de Udemy con cupón
                    titulo = post['text']
                    
                    # Verificar que sea una URL de Udemy con cupón
                    if 'udemy.com/course/' in udemy_url and 'couponCode=' in udemy_url:
                        # Extraer información del curso
                        course_name = extract_course_name(udemy_url)
                        # Extraer código de cupón de la URL
                        if 'couponCode=' in udemy_url:
                            coupon_code = udemy_url.split('couponCode=')[1].split('&')[0]
                        else:
                            coupon_code = "No encontrado"
                        
                        # Extraer la fuente del curso del texto
                        fuente = "CursosDev"
                        if "(IT & Software)" in post['text']:
                            fuente = "CursosDev (IT & Software)"
                        
                        curso = {
                            'titulo': f"{course_name}",
                            'url': udemy_url,  # URL completa de Udemy con cupón
                            'descripcion': f"Curso 100% gratis encontrado en {fuente} - Cupón: {coupon_code}",
                            'screenshot': None
                        }
                        
                        all_courses.append(curso)
                        print(f"✅ Curso agregado: {course_name}")
                        print(f"🎫 Cupón: {coupon_code}")
                        print(f"🔗 URL: {udemy_url}")
                    else:
                        print(f"⚠️ URL no válida o sin cupón en índice {i}: {udemy_url}")
                else:
                    print(f"⚠️ Post no válido en índice {i}: {post}")
                        
            except Exception as e:
                print(f"⚠️ Error procesando curso {i}: {e}")
        
        print(f"\n📊 RESUMEN:")
        print(f"Total de cursos CON CUPONES encontrados en CursosDev: {len(all_courses)}")
        print(f"  - De categoría IT & Software: {len(posts_categoria)}")
        print(f"  - De página principal: {len(posts_cursosdev)}")
        
        if not all_courses:
            print("❌ No se encontraron cursos CON CUPONES en CursosDev")
            print("Esto puede ser porque:")
            print("- No hay cursos disponibles en CursosDev")
            print("- Los enlaces no tienen cupones")
            print("- La página no cargó correctamente")
            return False
        
        # 3. ENVIAR POR WHATSAPP
        print(f"\nPASO 3: Enviando {len(all_courses)} cursos CON CUPONES por WhatsApp...")
        print("IMPORTANTE: Se aplicaran delays para evitar baneos")
        print("Se enviaran capturas de pantalla si estan disponibles")
        
        # Limitar a máximo 15 cursos para evitar baneos
        if len(all_courses) > 15:
            print(f"Limitando a 15 cursos para evitar baneos (encontrados: {len(all_courses)})")
            all_courses = all_courses[:15]
        
        # Enviar a grupo (cambia "contacto" por "grupo" si quieres enviar a grupo)
        success = enviar_cursos_sin_emojis(all_courses, destino="grupo")
        
        if success:
            print(f"\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
            print(f"✅ Cursos de Udemy CON CUPONES extraidos de CursosDev: {len(all_courses)}")
            print(f"✅ Mensaje enviado por WhatsApp")
            return True
        else:
            print("❌ Error enviando por WhatsApp")
            return False
    
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

def main():
    """Función principal"""
    try:
        success = run_bot_envio_directo()
        if success:
            print("\n🎯 ¡MISIÓN CUMPLIDA!")
            print("El bot ha extraido cursos CON CUPONES y los ha enviado por WhatsApp")
        else:
            print("\n💥 Error en la ejecucion")
            print("Revisa los logs para mas detalles")
    except Exception as e:
        print(f"💥 Error crítico: {e}")

if __name__ == "__main__":
    main() 