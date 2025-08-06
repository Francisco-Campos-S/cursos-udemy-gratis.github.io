# 🎓 Bot de Cursos Udemy - GitHub Pages

Este proyecto extrae cursos gratuitos de Udemy con cupones de CursosDev, toma capturas de pantalla y los publica automáticamente en GitHub Pages.

## 🚀 Características

- ✅ **Extracción automática** de cursos de CursosDev
- 📸 **Capturas de pantalla** de cada curso
- 🎫 **Códigos de cupón** incluidos
- 🌐 **Página web moderna** con diseño responsive
- 🤖 **Automatización completa** con GitHub Actions
- 📊 **Estadísticas en tiempo real**

## 📋 Requisitos

- Python 3.8+
- Google Chrome
- Cuenta de GitHub
- Repositorio público en GitHub

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar el repositorio:**
```bash
git init
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

## 🎯 Uso

### Extracción Manual

Para extraer cursos y crear la página web:

```bash
python extract_and_publish.py
```

Esto creará:
- `docs/index.html` - Página web principal
- `docs/courses.json` - Datos de los cursos
- `docs/README.md` - Documentación
- `screenshots/` - Capturas de pantalla

### Publicación Automática

Para configurar y publicar en GitHub Pages:

```bash
python github_publisher.py
```

Este script:
- Configura GitHub Pages
- Crea workflows de automatización
- Sube los cambios al repositorio

## 🌐 Configuración de GitHub Pages

1. **Ve a Settings > Pages** en tu repositorio
2. **Selecciona "GitHub Actions"** como fuente
3. **La página se publicará automáticamente**

### URL de tu página:
```
https://TU_USUARIO.github.io/TU_REPOSITORIO/
```

## 🤖 Automatización

El proyecto incluye workflows de GitHub Actions que:

- **Se ejecutan diariamente** a las 8:00 AM UTC
- **Extraen nuevos cursos** automáticamente
- **Toman capturas de pantalla** de cada curso
- **Actualizan la página web** automáticamente
- **Publican los cambios** en GitHub Pages

### Workflows incluidos:

1. **`auto-extract.yml`** - Extracción y actualización automática
2. **`deploy.yml`** - Despliegue a GitHub Pages

## 📁 Estructura del Proyecto

```
├── extract_and_publish.py      # Script principal de extracción
├── github_publisher.py         # Script de publicación
├── bot_principal_simple_fixed.py  # Bot original de WhatsApp
├── send_cursos_sin_emojis.py   # Envío por WhatsApp
├── config.py                   # Configuración
├── requirements.txt            # Dependencias
├── docs/                       # Archivos para GitHub Pages
│   ├── index.html             # Página web principal
│   ├── courses.json           # Datos de cursos
│   └── README.md              # Documentación
├── screenshots/                # Capturas de pantalla
└── .github/workflows/          # Workflows de GitHub Actions
    ├── auto-extract.yml        # Automatización
    └── deploy.yml              # Despliegue
```

## 🎨 Características de la Página Web

- **Diseño moderno** con gradientes y efectos visuales
- **Responsive** - Se adapta a móviles y tablets
- **Capturas de pantalla** incrustadas en base64
- **Códigos de cupón** destacados
- **Enlaces directos** a los cursos
- **Estadísticas** en tiempo real
- **Actualización automática** diaria

## 📊 Ejemplo de Salida

La página web mostrará:

```
🎓 Cursos Gratuitos de Udemy
📊 Estadísticas
Total de cursos disponibles: 15
Última actualización: 15/12/2024 14:30

[Curso 1] 📸 [Captura] 🎫 CUPON123 → Obtener Curso Gratis
[Curso 2] 📸 [Captura] 🎫 CUPON456 → Obtener Curso Gratis
...
```

## 🔧 Personalización

### Modificar el diseño

Edita la función `create_html_page()` en `extract_and_publish.py` para cambiar:
- Colores y estilos
- Layout y disposición
- Información mostrada

### Cambiar la fuente de cursos

Modifica la función `extract_courses_with_screenshots()` para:
- Extraer de otras fuentes
- Cambiar el número máximo de cursos
- Modificar los selectores de búsqueda

### Ajustar la automatización

Edita los workflows en `.github/workflows/` para:
- Cambiar la frecuencia de ejecución
- Modificar el horario de actualización
- Agregar más pasos de procesamiento

## 🚨 Solución de Problemas

### Error: "No se encontraron cursos"

- Verifica la conexión a internet
- Comprueba que CursosDev esté accesible
- Revisa los logs para más detalles

### Error: "Chrome no encontrado"

- Instala Google Chrome
- Asegúrate de que esté en el PATH del sistema

### Error: "GitHub Pages no funciona"

- Verifica que el repositorio sea público
- Comprueba que GitHub Pages esté habilitado
- Revisa los workflows en Actions

### Error: "Workflow falló"

- Ve a Actions en tu repositorio
- Revisa los logs del workflow fallido
- Verifica que las dependencias estén correctas

## 📝 Notas Importantes

- **Los cupones tienen tiempo limitado** de validez
- **La extracción puede tardar** varios minutos
- **Las capturas de pantalla** aumentan el tamaño del repositorio
- **GitHub Actions** tiene límites de tiempo de ejecución

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **CursosDev** por proporcionar los cursos gratuitos
- **GitHub** por GitHub Pages y Actions
- **Selenium** por la automatización web

---

**¡Disfruta de los cursos gratuitos! 🎓** 