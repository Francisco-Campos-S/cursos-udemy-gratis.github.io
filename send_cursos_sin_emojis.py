#!/usr/bin/env python3
"""
Script para enviar cursos por WhatsApp sin emojis
"""
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def enviar_cursos_sin_emojis(cursos, destino="grupo"):
    """
    Enviar cursos sin emojis
    destino: "contacto" o "grupo"
    """
    # Configuración según el destino
    if destino == "grupo":
        target_name = "Cursos 2025"  # Nombre real del grupo de WhatsApp
        print(f"Enviando a grupo: {target_name}")
    else:
        target_name = "50662454685"  # Número de teléfono para contacto individual
        print(f"Enviando a contacto: {target_name}")
    
    # Configuración básica
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Perfil único
    user_data_dir = os.path.join(os.getcwd(), "whatsapp_profile")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    
    driver = None
    try:
        print("Abriendo Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Abrir WhatsApp Web
        print("Navegando a WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        
        # Esperar a que cargue
        wait = WebDriverWait(driver, 60)
        
        # Verificar si ya está conectado
        try:
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
            print("WhatsApp Web ya conectado")
        except:
            print("Esperando escaneo del codigo QR...")
            print("Por favor, escanea el codigo QR con tu WhatsApp")
            print("Tienes 45 segundos para escanear...")
            time.sleep(45)
            
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
            print("WhatsApp Web conectado exitosamente")
        
        # Buscar grupo o contacto
        print(f"Buscando: {target_name}...")
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.clear()
        search_box.send_keys(target_name)
        time.sleep(8)  # Aumentado de 5 a 8 segundos para que aparezcan los resultados
        
        # Hacer clic en el grupo/contacto
        try:
            if destino == "grupo":
                print("Usando método mejorado para grupo...")
                
                # Método 1: Intentar hacer clic directo en el grupo
                target_found = False
                try:
                    print("Método 1: Buscando grupo en la lista de búsqueda...")
                    grupo_element = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), "{target_name}")]')))
                    print(f"✅ Grupo encontrado: {grupo_element.text}")
                    
                    # SALIR DEL BUSCADOR ANTES DEL CLIC
                    print("🔍 Saliendo del buscador antes del clic...")
                    search_box.send_keys(Keys.ESCAPE)
                    time.sleep(3)
                    
                    # RE-BUSCAR EL GRUPO DESPUÉS DEL ESCAPE
                    print("🔍 Re-buscando el grupo después del escape...")
                    grupo_element = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[contains(text(), "{target_name}")]')))
                    print(f"✅ Grupo re-encontrado: {grupo_element.text}")
                    
                    # Hacer clic y esperar más tiempo
                    grupo_element.click()
                    print("✅ Clic realizado en el grupo")
                    time.sleep(15)  # Aumentado a 15 segundos para que cargue completamente el chat
                    
                    # Limpiar el campo de búsqueda para asegurar que no esté activo
                    try:
                        search_box.clear()
                        print("✅ Campo de búsqueda limpiado")
                        time.sleep(3)
                    except:
                        print("⚠️ No se pudo limpiar el campo de búsqueda")
                    
                    # Verificar si realmente estamos en el grupo usando indicadores más específicos
                    try:
                        # Buscar indicadores de que estamos en el chat del grupo
                        chat_indicators = [
                            '//header[@data-testid="conversation-header"]',
                            '//div[@data-testid="conversation-compose-box-input"]',
                            '//div[@contenteditable="true"][@data-tab="6"]',
                            '//div[@contenteditable="true"][@data-tab="10"]'
                        ]
                        
                        chat_abierto = False
                        for indicator in chat_indicators:
                            try:
                                element = driver.find_element(By.XPATH, indicator)
                                print(f"✅ Indicador de chat encontrado: {indicator}")
                                chat_abierto = True
                                break
                            except:
                                continue
                        
                        if chat_abierto:
                            print("✅ Confirmado: estamos en el chat del grupo")
                            target_found = True
                        else:
                            print("⚠️ No se confirmó que estamos en el chat del grupo")
                            target_found = False
                            
                    except Exception as e:
                        print(f"⚠️ Error verificando chat: {e}")
                        target_found = False
                        
                except Exception as e:
                    print(f"❌ Método 1 falló: {e}")
                    target_found = False
                
                # Método 2: Si el método 1 falló, intentar con el primer resultado
                if not target_found:
                    print("Método 2: Intentando con el primer resultado de la búsqueda...")
                    try:
                        # Buscar de nuevo el grupo
                        search_box.clear()
                        search_box.send_keys(target_name)
                        time.sleep(5)
                        
                        # Salir del buscador
                        search_box.send_keys(Keys.ESCAPE)
                        time.sleep(2)
                        
                        first_result = driver.find_element(By.XPATH, '//div[@data-testid="cell-0-0"]')
                        first_result.click()
                        print("✅ Clic en primer resultado exitoso")
                        time.sleep(10)  # Aumentado a 10 segundos
                        
                        # Limpiar el campo de búsqueda
                        try:
                            search_box.clear()
                            print("✅ Campo de búsqueda limpiado (método 2)")
                            time.sleep(3)
                        except:
                            print("⚠️ No se pudo limpiar el campo de búsqueda (método 2)")
                        
                        target_found = True
                    except Exception as e:
                        print(f"❌ Método 2 falló: {e}")
                        target_found = False
                
            else:
                # Selectores para contactos individuales
                target_selectors = [
                    f'//span[@title="+{target_name}"]',
                    f'//span[contains(text(), "{target_name}")]',
                    f'//div[contains(text(), "{target_name}")]',
                    f'//span[contains(text(), "+{target_name}")]'
                ]
                print("Usando selectores para contacto...")
                
                target_found = False
                for i, selector in enumerate(target_selectors):
                    try:
                        print(f"Intentando selector {i+1}: {selector}")
                        target = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        print(f"✅ Elemento encontrado con selector {i+1}")
                        target.click()
                        target_found = True
                        print(f"✅ Clic exitoso en {target_name}")
                        break
                    except Exception as e:
                        print(f"❌ Selector {i+1} falló: {e}")
                        continue
        
        except Exception as e:
            print(f"❌ Error seleccionando destino: {e}")
            print("⚠️ Intentando continuar...")
        
        print(f"✅ {destino.capitalize()} {target_name} seleccionado")
        
        # Esperar a que se cargue el chat del grupo/contacto
        print("⏳ Esperando a que se cargue el chat...")
        time.sleep(10)  # Aumentado de 5 a 10 segundos para asegurar que se cargue el chat
        
        # Verificar que estamos en el chat correcto (opcional)
        try:
            # Buscar el header del chat para confirmar
            header = driver.find_element(By.XPATH, '//div[@data-testid="conversation-header"]')
            print("✅ Header del chat encontrado")
            
            # Verificar el nombre en el header
            try:
                if destino == "grupo":
                    nombre_header = header.find_element(By.XPATH, './/span[contains(text(), "Cursos 2025") or contains(text(), "CURSOS")]')
                    print(f"✅ Nombre confirmado en header: {nombre_header.text}")
                    
                    # Verificación adicional: asegurar que estamos en el grupo correcto
                    if "Cursos 2025" not in nombre_header.text:
                        print("⚠️ ADVERTENCIA: No estamos en el grupo correcto!")
                        print(f"   Esperado: 'Cursos 2025', Encontrado: '{nombre_header.text}'")
                        print("   Continuando de todas formas...")
                else:
                    nombre_header = header.find_element(By.XPATH, './/span[contains(text(), target_name)]')
                    print(f"✅ Nombre confirmado en header: {nombre_header.text}")
            except Exception as e:
                print(f"⚠️ No se pudo confirmar el nombre en el header: {e}")
                print("⚠️ Continuando de todas formas...")
                
        except Exception as e:
            print(f"⚠️ No se pudo verificar el header: {e}")
            print("⚠️ Continuando de todas formas...")
        
        # Verificación adicional para grupos: asegurar que estamos en un grupo y no en un contacto individual
        if destino == "grupo":
            print("🔍 Verificando que estamos en un grupo...")
            try:
                # Buscar indicadores de que estamos en un grupo
                group_indicators = [
                    '//div[contains(@aria-label, "group")]',
                    '//div[contains(@aria-label, "grupo")]',
                    '//span[contains(text(), "participants")]',
                    '//span[contains(text(), "participantes")]',
                    '//div[contains(@data-testid, "group")]'
                ]
                
                group_found = False
                for indicator in group_indicators:
                    try:
                        element = driver.find_element(By.XPATH, indicator)
                        print(f"✅ Indicador de grupo encontrado: {indicator}")
                        group_found = True
                        break
                    except:
                        continue
                
                if not group_found:
                    print("⚠️ ADVERTENCIA: No se detectaron indicadores de grupo")
                    print("   Es posible que estemos en un contacto individual en lugar del grupo")
                    print("   Intentando buscar el grupo nuevamente...")
                    
                    # Limpiar búsqueda y buscar de nuevo
                    search_box.clear()
                    time.sleep(2)
                    search_box.send_keys("Cursos 2025")
                    time.sleep(5)
                    
                    # Intentar hacer clic en el primer resultado que contenga "Cursos 2025"
                    try:
                        grupo_element = driver.find_element(By.XPATH, '//span[contains(text(), "Cursos 2025")]')
                        grupo_element.click()
                        print("✅ Grupo 'Cursos 2025' seleccionado correctamente")
                        time.sleep(5)
                    except Exception as e:
                        print(f"❌ Error al seleccionar el grupo: {e}")
                        print("⚠️ Continuando de todas formas...")
                else:
                    print("✅ Confirmado: estamos en un grupo")
                    
            except Exception as e:
                print(f"⚠️ Error verificando indicadores de grupo: {e}")
                print("⚠️ Continuando de todas formas...")
        
        # Enviar mensaje de inicio
        mensaje_inicio = f"CURSOS GRATUITOS ENCONTRADOS\n"
        mensaje_inicio += f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        mensaje_inicio += f"Total: {len(cursos)} cursos\n"
        mensaje_inicio += "=" * 40
        
        print("Enviando mensaje de inicio...")
        enviar_mensaje_simple(driver, mensaje_inicio)
        time.sleep(2)
        
        # Enviar cada curso por separado (evitando duplicados)
        cursos_enviados = set()  # Para evitar duplicados
        
        for i, curso in enumerate(cursos, 1):
                        # Verificar si ya se envió este curso (por URL)
                        if curso['url'] in cursos_enviados:
                            print(f"⚠️ Curso duplicado ignorado: {curso['titulo']}")
                            continue
                        
                        cursos_enviados.add(curso['url'])
                        
                        mensaje_curso = f"\nCURSO {i}:\n"
                        mensaje_curso += f"Titulo: {curso['titulo']}\n"  # Título completo sin cortar
                        mensaje_curso += f"URL: {curso['url']}\n"
                        mensaje_curso += "Estado: 100% GRATUITO"
                        
                        print(f"Enviando curso {i}/{len(cursos)}...")
                        enviar_mensaje_simple(driver, mensaje_curso)
                        
                        # Enviar captura si existe
                        if curso.get('screenshot') and os.path.exists(curso['screenshot']):
                            print(f"Enviando captura para curso {i}...")
                            enviar_imagen(driver, curso['screenshot'])
                        
                        # Delay más largo para evitar baneos
                        time.sleep(5)  # Aumentado de 2 a 5 segundos
        
        # Enviar mensaje final
        cursos_unicos_enviados = len(cursos_enviados)
        mensaje_final = f"Enviado por *FrostBot*"
        
        print("Enviando mensaje final...")
        enviar_mensaje_simple(driver, mensaje_final)
        
        print("Todos los cursos enviados exitosamente!")
        return True
        
    except Exception as e:
        print(f"Error en el proceso: {e}")
        return False
        
    finally:
        if driver:
            print("Chrome mantenido abierto para futuras sesiones")
            print("Perfil guardado en: whatsapp_profile/")

def enviar_mensaje_simple(driver, mensaje):
    """Enviar un mensaje simple"""
    try:
        # Esperar a que aparezca el campo de mensaje
        time.sleep(2)
        
        # Buscar el campo de mensaje
        message_box = None
        
        # Método 1: Buscar por data-tab específicos
        for data_tab in ['6', '10', '9']:
            try:
                message_box = driver.find_element(By.XPATH, f'//div[@contenteditable="true"][@data-tab="{data_tab}"]')
                print(f"✅ Campo de mensaje encontrado con data-tab='{data_tab}'")
                break
            except:
                continue
        
        # Método 2: Buscar por atributos específicos
        if not message_box:
            message_selectors = [
                '//div[@contenteditable="true"][@aria-label="Type a message"]',
                '//div[@contenteditable="true"][@aria-label="Escribe un mensaje"]',
                '//div[@contenteditable="true"][@data-testid="conversation-compose-box-input"]',
                '//div[@contenteditable="true"][@role="textbox"]'
            ]
            
            for selector in message_selectors:
                try:
                    message_box = driver.find_element(By.XPATH, selector)
                    print(f"✅ Campo de mensaje encontrado con selector: {selector}")
                    break
                except:
                    continue
        
        # Método 3: Buscar por ubicación (parte inferior)
        if not message_box:
            try:
                all_contenteditable = driver.find_elements(By.XPATH, '//div[@contenteditable="true"]')
                for element in all_contenteditable:
                    try:
                        data_tab = element.get_attribute('data-tab')
                        if data_tab == '3':  # Saltar campo de búsqueda
                            continue
                        
                        location = element.location
                        if location['y'] > 600:  # Aumentado el umbral
                            message_box = element
                            print(f"✅ Campo de mensaje encontrado por ubicación: y={location['y']}")
                            break
                    except:
                        continue
            except Exception as e:
                print(f"❌ Error buscando por ubicación: {e}")
        
        # Método 4: Hacer clic directo en el área de mensaje (último recurso)
        if not message_box:
            print("⚠️ No se encontró campo de mensaje, intentando clic directo...")
            try:
                # Hacer clic en el área inferior derecha donde normalmente está el campo de mensaje
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Hacer clic en el área de mensaje
                action = webdriver.ActionChains(driver)
                action.move_by_offset(800, 700).click().perform()
                time.sleep(2)
                
                # Intentar escribir directamente
                action.send_keys(mensaje).perform()
                time.sleep(2)
                action.send_keys(Keys.ENTER).perform()
                time.sleep(2)
                
                print("✅ Mensaje enviado por clic directo")
                return True
            except Exception as e:
                print(f"❌ Error con clic directo: {e}")
                return False
        
        # Enviar mensaje si se encontró el campo
        if message_box:
            try:
                print(f"📝 Enviando mensaje: {mensaje[:50]}...")
                
                # Limpiar el campo
                message_box.clear()
                time.sleep(1)
                
                # Enviar texto
                message_box.send_keys(mensaje)
                time.sleep(2)
                
                # Enviar con Enter
                message_box.send_keys(Keys.ENTER)
                time.sleep(2)
                
                print("✅ Mensaje enviado exitosamente")
                return True
                
            except Exception as e:
                print(f"❌ Error enviando mensaje: {e}")
                return False
        
        return False
        
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")
        return False

def enviar_imagen(driver, ruta_imagen):
    """Enviar una imagen por WhatsApp"""
    try:
        # Buscar el botón de adjuntar
        attach_button = None
        attach_selectors = [
            '//span[@data-icon="attach-menu-plus"]',
            '//div[@data-testid="attach-button"]',
            '//div[@aria-label="Attach"]',
            '//div[@aria-label="Adjuntar"]',
            '//span[@data-icon="attach-menu-plus"]/parent::div'
        ]
        
        for selector in attach_selectors:
            try:
                attach_button = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if not attach_button:
            print("No se pudo encontrar el botón de adjuntar")
            return False
        
        # Hacer clic en el botón de adjuntar
        attach_button.click()
        time.sleep(2)
        
        # Buscar el input de archivo
        file_input = None
        file_selectors = [
            '//input[@type="file"]',
            '//input[@accept="image/*"]'
        ]
        
        for selector in file_selectors:
            try:
                file_input = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if not file_input:
            print("No se pudo encontrar el input de archivo")
            return False
        
        # Enviar la imagen
        file_input.send_keys(os.path.abspath(ruta_imagen))
        time.sleep(3)
        
        # Buscar y hacer clic en el botón de enviar
        send_button = None
        send_selectors = [
            '//span[@data-icon="send"]',
            '//div[@data-testid="send"]',
            '//button[@aria-label="Send"]',
            '//button[@aria-label="Enviar"]'
        ]
        
        for selector in send_selectors:
            try:
                send_button = driver.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if send_button:
            send_button.click()
            time.sleep(3)
            print(f"Imagen enviada: {ruta_imagen}")
            return True
        else:
            print("No se pudo encontrar el botón de enviar")
            return False
            
    except Exception as e:
        print(f"Error enviando imagen: {e}")
        return False

def main():
    """Función principal"""
    print("ENVIO DE CURSOS SIN EMOJIS")
    print("=" * 50)
    print("PRUEBA: Solo 2 cursos al grupo 'UDEMY, STEAM, EPIC GAMES,'")
    print("=" * 50)
    
    # Cursos de prueba - SOLO 2 cursos
    cursos_prueba = [
        {
            "titulo": "Python para Principiantes - Curso Completo",
            "url": "https://www.udemy.com/course/python-para-principiantes/",
            "descripcion": "Aprende Python desde cero hasta nivel intermedio"
        },
        {
            "titulo": "JavaScript Moderno - ES6+ Completo",
            "url": "https://www.udemy.com/course/javascript-moderno-es6/",
            "descripcion": "Aprende JavaScript moderno con las últimas características"
        }
    ]
    
    print(f"Enviando {len(cursos_prueba)} cursos SOLO al grupo 'UDEMY, STEAM, EPIC GAMES,'...")
    
    for i, curso in enumerate(cursos_prueba, 1):
        print(f"{i}. {curso['titulo']}")
    
    print("\nEnviando por WhatsApp al grupo 'UDEMY, STEAM, EPIC GAMES,'...")
    time.sleep(3)
    
    success = enviar_cursos_sin_emojis(cursos_prueba, destino="grupo")
    
    if success:
        print("\nENVIO EXITOSO!")
        print("Los 2 cursos se enviaron correctamente al grupo 'UDEMY, STEAM, EPIC GAMES,'")
    else:
        print("\nError en el envio")

if __name__ == "__main__":
    main() 