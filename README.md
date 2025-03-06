
# 📝 Generador de README Automático con IA

Un generador de `README.md` impulsado por **Gemini AI** que analiza el código de un proyecto y genera un README completo con tecnologías, estructura y pasos de instalación.

## 🚀 Características

✅  **Detección Automática** : Extrae tecnologías y estructura del proyecto.

✅  **Personalización** : Puedes elegir idioma, nivel de detalle y contenido adicional.

✅  **Interfaz CLI** : Simple y fácil de usar desde la terminal.

✅  **Evita Sobreescribir** : Pregunta antes de reemplazar un README existente.

✅  **Estilos Personalizados** : Genera README detallados, minimalistas o técnicos.

---

## 📚 Instalación

Puedes instalar y usar el generador de README de dos maneras:

### **1️⃣ Instalación Manual**

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/readme-generator.git
cd readme-generator

# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar Gemini AI (Requiere API Key de Google)
export GEMINI_API_KEY="TU_API_KEY"  # Linux/macOS
set GEMINI_API_KEY="TU_API_KEY"  # Windows
```

### **2️⃣ Instalación Global como CLI**

Si deseas instalar el generador globalmente para ejecutarlo desde cualquier carpeta:

```bash
pip install .

# Configurar la API Key de Gemini AI
export GEMINI_API_KEY="TU_API_KEY"  # Linux/macOS
set GEMINI_API_KEY="TU_API_KEY"  # Windows
```

Esto te permitirá usarlo en cualquier proyecto con el siguiente comando:

```bash
readme-gen
```

---

## 📌 Configuración Inicial

La primera vez que ejecutes el generador, te hará algunas preguntas para personalizar tu `README.md`. Estas incluyen:

* **Nombre del Proyecto**
* **Descripción del Proyecto**
* **Idioma del README**
* **Incluir capturas de pantalla? (y/n)**
* **Incluir estadísticas de GitHub? (y/n)**
* **Pasos de instalación personalizados?**
* **Ejemplo de uso**

Toda esta configuración se guardará en un archivo `readme-config.json`, que puedes editar manualmente más tarde.

Ejemplo de `readme-config.json`:

```json
{
  "project_name": "Nombre del Proyecto",
  "project_description": "Descripción del proyecto",
  "language": "es",
  "readme_style": "detailed",
  "include_screenshots": true,
  "include_github_stats": true,
  "github_repo": "TU_USUARIO/TU_REPO"
}
```

Opciones de  **`readme_style`** : `detailed` | `minimal` | `technical`

Para regenerar el `README.md` con la configuración guardada:

```bash
readme-gen --regenerate
```

---

## 📀 Uso Rápido

Generar un README en la carpeta actual:

```bash
python readme-generator/generate_readme.py
```

Si ya existe un `README.md`, el sistema preguntará antes de sobrescribirlo. Para forzar la regeneración:

```bash
python readme-generator/generate_readme.py --force
```

Si usaste la instalación como CLI:

```bash
readme-gen
```

---

## 🛠️ Tecnologías Usadas

* **Python** 🐍
* **Google Gemini AI** 🤖
* **Rich** (para salida en terminal) 🎨

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 🛠️

1. Haz un fork del repositorio
2. Crea una rama con tu mejora (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de los cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Sube los cambios (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request 🚀

---

## 📝 Licencia

Este proyecto está bajo la  **Licencia MIT** . Consulta el archivo `LICENSE` para más detalles.

---

## 📲 Contacto

Si tienes dudas o sugerencias, puedes contactarme en:

📧 Email: [tuemail@ejemplo.com](mailto:tuemail@ejemplo.com)

🔗 LinkedIn: [linkedin.com/in/tuperfil](https://linkedin.com/in/tuperfil)
