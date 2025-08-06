# Bot Mejorado - 10 Cursos Gratuitos de Udemy

## 🎯 Descripción

Bot mejorado que busca exactamente **10 cursos gratuitos** de Udemy en CursosDev, toma capturas de pantalla enfocadas y pequeñas, y los publica automáticamente en GitHub Pages.

## ✨ Características Mejoradas

- **🎯 Búsqueda precisa**: Encuentra exactamente 10 cursos gratuitos
- **📸 Capturas enfocadas**: Toma capturas pequeñas enfocadas en elementos que indican "100% gratis"
- **🔍 Verificación mejorada**: Verifica claramente cuando un curso es realmente gratis
- **🌐 Publicación automática**: Crea y publica una página web en GitHub Pages
- **📱 Diseño responsive**: Página web moderna y responsive

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 2. Instalar dependencias
```bash
pip install selenium Pillow webdriver-manager
```

### 3. Configurar Git (si no está configurado)
```bash
git init
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

## 🎮 Uso

### Ejecución Simple
```bash
python ejecutar_bot_10_cursos.py
```

### Ejecución Directa
```bash
python bot_mejorado_10_cursos.py
```

## 📋 Proceso del Bot

### Paso 1: Inicialización
- Verifica dependencias instaladas
- Inicializa el navegador Chrome
- Configura opciones anti-detección

### Paso 2: Extracción de Cursos
- Navega a CursosDev.com
- Busca enlaces de cursos con cupones
- Procesa cada enlace hasta encontrar 10 cursos válidos
- Verifica que cada curso sea realmente gratis

### Paso 3: Capturas Enfocadas
- Busca elementos específicos que indiquen "100% gratis"
- Toma capturas enfocadas en esos elementos
- Redimensiona las imágenes para que sean más pequeñas (máximo 400px de ancho)
- Optimiza la calidad de las imágenes

### Paso 4: Creación de Página Web
- Crea una página HTML moderna y responsive
- Incluye todas las capturas de pantalla
- Muestra códigos de cupón y enlaces directos
- Diseño atractivo con gradientes y animaciones

### Paso 5: Publicación en GitHub
- Hace commit de todos los cambios
- Sube automáticamente a GitHub
- La página estará disponible en GitHub Pages

## 📸 Características de las Capturas

### Capturas Enfocadas
- **Tamaño máximo**: 400px de ancho
- **Enfoque**: Elementos que indican "100% gratis"
- **Optimización**: Calidad 85% para reducir tamaño
- **Formato**: PNG con compresión

### Elementos Detectados
- Botones "Inscribirse gratis"
- Texto "100% gratis" o "100% free"
- Precios "$0" o "0€"
- Indicadores de cursos gratuitos

## 🌐 Página Web Generada

### Características
- **Diseño moderno**: Gradientes y efectos visuales
- **Responsive**: Se adapta a móviles y tablets
- **Información completa**: Títulos, cupones, enlaces
- **Estadísticas**: Número de cursos y última actualización

### Estructura
```
docs/
└── index.html          # Página principal
```

## 📊 Resultados Esperados

### Cursos Encontrados
- **Cantidad**: Exactamente 10 cursos
- **Calidad**: Todos verificados como 100% gratis
- **Cupones**: Códigos de cupón incluidos
- **Enlaces**: URLs directas a Udemy

### Página Web
- **URL**: `https://TU_USUARIO.github.io/TU_REPOSITORIO/`
- **Contenido**: 10 cursos con capturas y cupones
- **Actualización**: Automática con cada ejecución

## 🔧 Configuración Avanzada

### Modificar Número de Cursos
En `bot_mejorado_10_cursos.py`, línea 400:
```python
courses = extraer_cursos_de_cursosdev(driver, max_cursos=10)  # Cambiar 10 por el número deseado
```

### Modificar Tamaño de Capturas
En `bot_mejorado_10_cursos.py`, línea 120:
```python
max_width = 400  # Cambiar por el ancho máximo deseado
```

### Personalizar Diseño Web
Editar la función `create_html_page()` en `bot_mejorado_10_cursos.py` para modificar el CSS y HTML.

## 🐛 Solución de Problemas

### Error: "No es un repositorio Git"
```bash
git init
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

### Error: "Faltan dependencias"
```bash
pip install selenium Pillow webdriver-manager
```

### Error: "No se encontraron cursos"
- Verificar conexión a internet
- CursosDev puede estar temporalmente no disponible
- Intentar ejecutar nuevamente

### Error: "No se pudo subir a GitHub"
- Verificar credenciales de Git
- Verificar permisos del repositorio
- Verificar conexión a internet

## 📈 Monitoreo

### Logs del Bot
El bot muestra información detallada durante la ejecución:
- ✅ Cursos encontrados
- 📸 Capturas tomadas
- 🔗 URLs procesadas
- 📊 Estadísticas finales

### Verificación de Resultados
1. Revisar la consola para confirmar 10 cursos encontrados
2. Verificar que se creó el archivo `docs/index.html`
3. Confirmar que se subieron los cambios a GitHub
4. Visitar la página en GitHub Pages

## 🔄 Automatización

### GitHub Actions
Para automatizar la ejecución diaria, crear el archivo `.github/workflows/auto-extract.yml`:

```yaml
name: Auto Extract Courses

on:
  schedule:
    - cron: '0 8 * * *'  # Diario a las 8:00 AM UTC
  workflow_dispatch:     # Ejecución manual

jobs:
  extract-courses:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - run: |
        pip install selenium Pillow webdriver-manager
        python bot_mejorado_10_cursos.py
    - run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git diff --quiet && git diff --staged --quiet || git commit -m "Auto-update courses $(date)"
        git push
```

## 📝 Notas Importantes

### Limitaciones
- Requiere conexión a internet
- Depende de la disponibilidad de CursosDev
- Puede tomar varios minutos en completarse
- Requiere Chrome instalado

### Recomendaciones
- Ejecutar en horarios de baja actividad
- Monitorear los logs para detectar problemas
- Verificar regularmente que la página web funcione
- Hacer backup de configuraciones importantes

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas:
1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Confirma que el repositorio Git esté configurado
4. Abre un issue en GitHub con detalles del problema

---

**¡Disfruta de los cursos gratuitos de Udemy! 🎓** 