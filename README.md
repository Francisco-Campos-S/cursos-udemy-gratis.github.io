# 🤖 Bot de Cursos Udemy

Bot automatizado para extraer y enviar cursos gratuitos de Udemy a grupos de WhatsApp.

## 📋 Descripción

Este bot automatiza la búsqueda y extracción de cursos gratuitos desde [CursosDev](https://cursosdev.com) y los envía automáticamente a un grupo específico de WhatsApp llamado "Cursos Udemy".

## ✨ Características

- 🔍 **Extracción automática** de cursos gratuitos desde CursosDev
- ✅ **Verificación de cursos** - Confirma que los cursos sean realmente gratuitos
- 📱 **Envío automático** a WhatsApp Web
- 🚫 **Prevención de duplicados** - No envía el mismo curso dos veces
- 🎯 **Envío a grupos** - Configurado para enviar al grupo "Cursos Udemy"
- 💾 **Sesión persistente** - Mantiene la sesión de WhatsApp Web

## 🛠️ Requisitos

- Python 3.7+
- Google Chrome
- Cuenta de WhatsApp
- Conexión a internet

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Francisco-Campos-S/Bot-de-cursos-Udemy.git
cd Bot-de-cursos-Udemy
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar el bot:**
   - Editar `config.py` si necesitas cambiar configuraciones
   - Asegurarte de tener Chrome instalado

## 🚀 Uso

### Ejecutar el bot principal:
```bash
python bot_principal_simple_fixed.py
```

### Configuración inicial:
1. Al ejecutar por primera vez, se abrirá WhatsApp Web
2. Escanea el código QR con tu teléfono
3. El bot mantendrá la sesión para futuras ejecuciones

## 📁 Estructura del Proyecto

```
Bot-de-cursos-Udemy/
├── bot_principal_simple_fixed.py    # Bot principal
├── send_cursos_sin_emojis.py        # Módulo de envío WhatsApp
├── config.py                        # Configuraciones
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── .gitignore                       # Archivos excluidos
├── whatsapp_profile/                # Perfil de Chrome (excluido)
└── logs/                           # Logs del bot (excluido)
```

## ⚙️ Configuración

### Archivo `config.py`:
```python
# Configuraciones del bot
MAX_COURSES = 10                    # Máximo de cursos a procesar
DELAY_BETWEEN_COURSES = 5          # Delay entre cursos (segundos)
VERIFICATION_DELAY = 8             # Delay para verificar curso gratuito
```

### Grupo de WhatsApp:
- **Nombre del grupo**: "Cursos Udemy"
- **Configuración**: El bot está configurado para enviar automáticamente a este grupo

## 🔧 Funcionalidades Técnicas

### Extracción de Cursos:
- Navega automáticamente por CursosDev
- Extrae título, descripción y URL del curso
- Verifica que el curso sea gratuito en Udemy
- Captura screenshot del curso

### Envío a WhatsApp:
- Busca automáticamente el grupo "Cursos Udemy"
- Envía mensaje con toda la información del curso
- Incluye screenshot del curso
- Previene envío de cursos duplicados

## 🛡️ Seguridad

- **Datos de sesión**: El directorio `whatsapp_profile/` está excluido del repositorio
- **Logs**: Los archivos de log se almacenan localmente
- **Screenshots**: Se guardan temporalmente y se limpian automáticamente

## 📝 Logs

El bot genera logs detallados de todas las operaciones:
- Extracción de cursos
- Verificación de cursos gratuitos
- Envío de mensajes
- Errores y excepciones

## 🐛 Solución de Problemas

### Bot no encuentra el grupo:
- Verifica que el grupo "Cursos Udemy" existe
- Asegúrate de estar en el grupo
- Revisa que WhatsApp Web esté conectado

### Bot no envía mensajes:
- Verifica la conexión a internet
- Revisa que Chrome esté actualizado
- Comprueba que la sesión de WhatsApp Web esté activa

### Cursos no se extraen:
- Verifica que CursosDev esté accesible
- Revisa la conexión a internet
- Comprueba que Chrome funcione correctamente

## 📄 Licencia

Este proyecto es de uso privado y personal.

## 👨‍💻 Autor

**Francisco Antonio Campos Sandi**
- Email: profesorfranciscocampos@gmail.com

## 🔄 Actualizaciones

- **v1.0**: Bot funcional con extracción y envío automático
- **v1.1**: Mejoras en detección de grupo WhatsApp
- **v1.2**: Prevención de duplicados y optimizaciones

---

**⚠️ Nota**: Este bot es para uso educativo y personal. Respeta los términos de servicio de las plataformas utilizadas. 