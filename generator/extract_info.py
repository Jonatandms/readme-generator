import json
import os
import re
from google import genai
from rich.console import Console

# 🔹 Máximo de caracteres que enviamos a la IA
MAX_TOKENS = 20000  # Aproximadamente 20K caracteres, para no superar los límites de Google AI

# 🔹 Extensiones de archivos que analizaremos
VALID_EXTENSIONS = (".py", ".js", ".ts", ".dart", ".cpp", ".java")

# 🔹 Directorios a ignorar
IGNORE_DIRS = ["node_modules", "venv", ".git", "dist", "__pycache__"]

console = Console()

def log_error(error_message):
    """Guarda errores en un archivo log para debugging."""
    with open("error_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{error_message}\n")


def get_gemini_analysis(code_snippets):
    config = load_config()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ ERROR: No se encontró la API Key. Configura la variable GEMINI_API_KEY.")

    client = genai.Client(api_key=api_key)

    try:
        # 📌 Construimos el prompt asegurándonos de que la IA genere todo el README en formato Markdown
        prompt = f"""
        Eres un experto en desarrollo de software y documentación técnica.
        Genera un **README.md profesional** en **{config.get("language", "es")}** con la siguiente información:

        - **Nombre del Proyecto:** {config.get("project_name", "Nombre no especificado")}
        - **Descripción:** {config.get("project_description", "Describe este proyecto de manera clara.")}
        - **Tecnologías Utilizadas:** Si no se especifican, **analiza el código y sugiere las más relevantes**.
        - **Estructura del Proyecto:** Usa el código proporcionado para generar un árbol de directorios.
        - **Cómo Instalarlo y Usarlo:** Si no se especifican pasos, **genéralos de acuerdo al código del proyecto**.
        - **Ejemplos de Uso:** Si no hay ejemplos, **crea uno basado en cómo funciona este código**.
        - **Notas Importantes:** Si el usuario no ha escrito nada, **sugiere advertencias relevantes**.
        - **Screenshots:** Si no hay imágenes, **sugiere capturas de pantalla de la interfaz**.
        - **Estadísticas de GitHub:** Si no se proporciona, **sugiere badges con estrellas, forks e issues**.
        - **Secciones Personalizadas:** Si no se especifican, **sugiere secciones como Contributing, License, etc.**.
        - **Tipo de Proyecto:** Si no se especifica, **analiza el código y sugiere el tipo de proyecto**.

        📂 **Código del Proyecto:** 
        {code_snippets}
        
        Configuración Personalizada:
        {json.dumps(config, indent=4)}

        📌 **Tu tarea es generar un README COMPLETO en formato Markdown.**
        **Si no hay información en alguna sección, usa tu conocimiento para llenarla.**
        **Responde ÚNICAMENTE en formato Markdown sin texto adicional.**
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        if not response or not response.text:
            console.print("[red]❌ ERROR: Gemini no generó ninguna respuesta válida.[/red]")
            log_error("ERROR: Gemini no generó ninguna respuesta válida.")
            return "Error: La IA no generó contenido.", "Desconocido", "README no generado."

        readme_content = response.text.strip()
        log_error(f"🔹 Respuesta completa de Gemini:\n{readme_content}")

        # 📌 **Eliminamos SOLO el primer y el último delimitador ` ```markdown ` y ` ``` `**
        readme_content = re.sub(r"^```markdown\n", "", readme_content, count=1)  # Elimina solo la PRIMERA aparición
        readme_content = re.sub(r"\n```$", "", readme_content, count=1)  # Elimina solo la ÚLTIMA aparición

        # 📌 **Si sigue habiendo menos de 20 caracteres, probablemente algo salió mal**
        if len(readme_content) < 20:
            console.print("[red]❌ ERROR: Gemini generó un README demasiado corto o vacío.[/red]")
            log_error(f"ERROR: README generado muy corto: {readme_content}")
            return "Error: README vacío.", "Desconocido", "README no generado."

        return readme_content, "Desconocido", readme_content  

    except Exception as e:
        error_message = f"❌ ERROR al generar el README con IA: {str(e)}"
        console.print(f"[red]{error_message}[/red]")
        log_error(error_message)
        return f"Error al generar la descripción: {str(e)}", "Desconocido", "README no generado."

    except Exception as e:
        error_message = f"❌ ERROR al generar el README con IA: {str(e)}"
        console.print(f"[red]{error_message}[/red]")
        log_error(error_message)
        return f"Error al generar la descripción: {str(e)}", "Desconocido", "README no generado."
    
def extract_all_code():
    """Recorre el proyecto, extrae fragmentos de código y optimiza el contenido enviado a la IA."""
    code_snippets = []
    total_size = 0

    for root, _, files in os.walk("."):
        if any(ignored in root for ignored in IGNORE_DIRS):
            continue

        for file in files:
            if file.endswith(VALID_EXTENSIONS):
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)

                if size > 1024 * 1024:
                    continue

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                fragment = content[:1000]  # 1000 caracteres por archivo
                code_snippets.append(f"### {file_path} ###\n{fragment}\n")

                total_size += len(fragment)
                if total_size > MAX_TOKENS:
                    break

    return "\n".join(code_snippets) if code_snippets else "No se encontró código relevante."

    
def get_screenshots_section():
    """Busca imágenes en 'screenshots/' o 'assets/' y genera la sección para el README."""
    image_formats = (".png", ".jpg", ".jpeg", ".gif")
    screenshot_dirs = ["screenshots", "assets"]
    screenshot_section = ""

    for directory in screenshot_dirs:
        if os.path.exists(directory):
            images = [f for f in os.listdir(directory) if f.endswith(image_formats)]
            if images:
                screenshot_lines = ["## 📸 Screenshots\n"]
                for image in images:
                    screenshot_lines.append(f"![{image}]({directory}/{image})\n")
                screenshot_section += "\n".join(screenshot_lines) + "\n"
                break  # Solo usamos la primera carpeta encontrada con imágenes

    return screenshot_section if screenshot_section else ""


def load_config():
    """Carga las configuraciones desde readme-config.json. Si no existe, pregunta al usuario por CLI."""
    config_path = "readme-config.json"
    
    # Si el archivo existe, lo cargamos
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Si no existe, pedimos la información al usuario
    print("\n📝 No se encontró 'readme-config.json'. Vamos a crearlo con tus respuestas.\n")

    project_name = input("📌 Nombre del Proyecto: ") or "My Project"
    project_description = input("📝 Descripción del Proyecto: ") or "Descripción generada automáticamente."
    language = input("🌎 Idioma del README (es/en/fr/etc.): ") or "es"
    include_screenshots = input("📸 ¿Incluir screenshots? (y/n): ").strip().lower() == "y"
    include_github_stats = input("📊 ¿Incluir stats de GitHub? (y/n): ").strip().lower() == "y"

    if include_github_stats:
        github_repo = input("🔗 URL del repo en GitHub (user/repo): ") or "user/repo"
    else:
        github_repo = ""

    print("\n⚙️ Pasos de instalación (deja vacío para terminar):")
    steps = []
    while True:
        step = input(f"   Paso {len(steps) + 1}: ")
        if step.strip() == "":
            break
        steps.append(step)
    installation_steps = "\n".join(steps)

    usage_example = input("\n▶️ Ejemplo de Uso (opcional): ") or ""
    important_notes = input("\n⚠️ Notas importantes (opcional): ") or ""

    # Secciones personalizadas
    custom_sections = {}
    print("\n➕ ¿Quieres agregar secciones personalizadas? (por ejemplo, 'License', 'Contributing', etc.)")
    while True:
        section_name = input("   Nombre de la Sección (deja vacío para terminar): ")
        if section_name.strip() == "":
            break
        section_content = input(f"   Contenido de '{section_name}': ")
        custom_sections[section_name] = section_content

    # Crear configuración final
    config = {
        "project_name": project_name,
        "project_description": project_description,
        "language": language,
        "include_screenshots": include_screenshots,
        "include_github_stats": include_github_stats,
        "github_repo": github_repo,
        "installation_steps": installation_steps,
        "usage_example": usage_example,
        "important_notes": important_notes,
        "custom_sections": custom_sections
    }

    # Guardar en readme-config.json
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print("\n✅ Archivo 'readme-config.json' creado con éxito!\n")
    return config


def get_project_info():
    """Extrae información del proyecto y usa IA para generar el README completo sin duplicaciones."""
    config = load_config()
    code_snippets = extract_all_code()
    readme_content, project_type, _ = get_gemini_analysis(code_snippets)

    # Usar valores personalizados del usuario si existen
    project_name = config.get("project_name", "Unknown Project")

    # 📌 Validar si la IA ya incluye un título para evitar duplicados
    if readme_content.startswith("# "):
        formatted_readme = readme_content
    else:
        formatted_readme = f"# {project_name}\n\n{readme_content}"

    return {
        "name": project_name,
        "description": config.get("project_description", "Descripción no generada."),
        "project_type": project_type or "Desconocido",
        "readme_content": formatted_readme,
    }
