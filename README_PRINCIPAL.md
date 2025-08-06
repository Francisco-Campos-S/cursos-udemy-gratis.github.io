# 🤖 Bot Completo de Cursos Udemy

Este repositorio contiene el bot completo para extraer cursos gratuitos de Udemy y publicarlos en GitHub Pages.

## 🌐 Página Web Publicada

**Visita la página web:** [https://Francisco-Campos-S.github.io/cursos-udemy-gratis.github.io/](https://Francisco-Campos-S.github.io/cursos-udemy-gratis.github.io/)

## 📁 Estructura del Proyecto

```
cursos-udemy-gratis/
├── 📄 Archivos de la página web:
│   ├── index.html              # Página web principal
│   ├── courses.json            # Datos de cursos
│   ├── screenshots/            # Capturas de pantalla
│   └── README.md               # README de la página web
│
├── 🤖 Scripts del bot:
│   ├── bot_principal_simple_fixed.py    # Bot principal (WhatsApp)
│   ├── extract_and_publish.py           # Extracción + GitHub Pages
│   ├── web_publisher.py                 # Publicación web
│   ├── run_web_only.py                  # Ejecutor web completo
│   ├── create_github_pages_repo.py      # Creador de repositorio
│   ├── upload_to_new_repo.py            # Subida a GitHub
│   ├── send_cursos_sin_emojis.py        # Envío WhatsApp
│   └── config.py                        # Configuraciones
│
├── 📋 Documentación:
│   ├── README_PRINCIPAL.md              # Este archivo
│   ├── README_WEB_ONLY.md               # Documentación web
│   ├── README_GITHUB_PAGES.md           # Documentación GitHub Pages
│   └── requirements.txt                 # Dependencias Python
│
└── ⚙️ Configuración:
    ├── .github/workflows/deploy.yml     # Workflow GitHub Pages
    └── .gitignore                       # Archivos a ignorar
```

## 🚀 Cómo usar el bot

### Opción 1: Solo Página Web (Recomendado)
```bash
python run_web_only.py
```
- Extrae cursos con capturas de pantalla
- Crea página web para GitHub Pages
- Publica automáticamente

### Opción 2: Bot Completo (WhatsApp + Web)
```bash
python bot_principal_simple_fixed.py
```
- Extrae cursos de CursosDev
- Envía a WhatsApp
- Toma capturas de pantalla

### Opción 3: Solo Extracción Web
```bash
python extract_and_publish.py
```
- Solo extrae y crea página web
- Sin envío a WhatsApp

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Francisco-Campos-S/cursos-udemy-gratis.github.io.git
cd cursos-udemy-gratis.github.io
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar (opcional):**
```bash
# Editar config.py si necesitas cambiar configuraciones
notepad config.py
```

## 🎯 Funcionalidades

### ✅ Extracción de Cursos
- Navega automáticamente por CursosDev
- Extrae título, descripción y URL del curso
- Verifica que el curso sea gratuito en Udemy
- Captura screenshot del curso

### 🌐 Publicación Web
- Genera página HTML moderna y responsive
- Incluye capturas de pantalla incrustadas
- Códigos de cupón destacados
- Diseño profesional y atractivo

### 📱 Envío WhatsApp (Opcional)
- Busca automáticamente el grupo "Cursos Udemy"
- Envía mensaje con toda la información del curso
- Incluye screenshot del curso
- Previene envío de cursos duplicados

### 🤖 Automatización
- GitHub Actions para despliegue automático
- Actualización diaria programada
- Workflow configurado para GitHub Pages

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

## 🔧 Scripts Principales

### `run_web_only.py`
- **Propósito**: Ejecutor principal para solo web
- **Funciones**: Extracción + Publicación web
- **Sin WhatsApp**: Solo GitHub Pages

### `extract_and_publish.py`
- **Propósito**: Extraer cursos y crear página web
- **Salida**: `index.html`, `courses.json`, screenshots
- **Sin WhatsApp**: Solo archivos web

### `bot_principal_simple_fixed.py`
- **Propósito**: Bot completo con WhatsApp
- **Funciones**: Extracción + WhatsApp + Screenshots
- **Con WhatsApp**: Envío automático a grupos

### `web_publisher.py`
- **Propósito**: Publicar en GitHub Pages
- **Funciones**: Git commands + GitHub Actions
- **Automatización**: Despliegue automático

## 📊 Características de la Página Web

- **Diseño moderno** con gradientes y efectos visuales
- **Responsive** - Se adapta a móviles y tablets
- **Capturas de pantalla** incrustadas en base64
- **Códigos de cupón** destacados con gradientes
- **Enlaces directos** a los cursos de Udemy
- **Estadísticas** en tiempo real
- **Diseño profesional** y atractivo

## 🔄 Actualización Automática

- **GitHub Actions**: Se ejecuta automáticamente al hacer push
- **Workflow configurado**: Despliega automáticamente en GitHub Pages
- **Actualización diaria**: La página se actualiza con cada cambio

## 🛡️ Seguridad

- **Datos de sesión**: El directorio `whatsapp_profile/` está excluido del repositorio
- **Logs**: Los archivos de log se almacenan localmente
- **Screenshots**: Se guardan temporalmente y se limpian automáticamente

## 📝 Notas Importantes

- Los cupones tienen tiempo limitado de validez
- Los cursos son extraídos de CursosDev
- La página web es solo informativa
- El bot puede funcionar con o sin WhatsApp

## 🤝 Contribuir

Si encuentras un curso que no funciona o quieres sugerir mejoras:

1. Ve a [Issues](https://github.com/Francisco-Campos-S/cursos-udemy-gratis.github.io/issues)
2. Crea un nuevo issue
3. Describe el problema o sugerencia

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¡Disfruta de los cursos gratuitos! 🎓**

**🌐 Página web:** [https://Francisco-Campos-S.github.io/cursos-udemy-gratis.github.io/](https://Francisco-Campos-S.github.io/cursos-udemy-gratis.github.io/) 