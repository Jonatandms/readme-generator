import argparse
import os
from generator.extract_info import get_project_info
from rich.console import Console

console = Console()

def generate_readme(output_file="README.md", force=False):
    """Genera el archivo README.md automáticamente en el directorio donde se ejecuta el comando."""
    console.print("[cyan]📄 Generando README con IA...[/cyan]")
    
    info = get_project_info()
    
    # 📌 Aseguramos que el contenido es un string válido antes de escribirlo
    readme_content = info["readme_content"]
    
    if not isinstance(readme_content, str) or len(readme_content.strip()) < 20:
        console.print("[red]❌ ERROR: El contenido generado por la IA es inválido o demasiado corto.[/red]")
        return

    # 📌 Guardar el README en el directorio donde el usuario ejecuta el comando
    output_path = os.path.join(os.getcwd(), output_file)

    if os.path.exists(output_path) and not force:
        overwrite = input("⚠️ Ya existe un README.md. ¿Quieres sobrescribirlo? (y/n): ").strip().lower()
        if overwrite != "y":
            console.print("[yellow]❌ Operación cancelada. El README existente no fue modificado.[/yellow]")
            return

    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    console.print(f"[green]✅ README.md generado con éxito en {output_path}![/green]")
    console.print(f"[yellow]📌 Tipo de Proyecto Detectado:[/yellow] {info['project_type']}")
    console.print(f"[blue]📖 Descripción General:[/blue] {info['description']}")

def main():
    parser = argparse.ArgumentParser(description="Generador de README Automático")
    parser.add_argument("--output", type=str, default="README.md", help="Nombre del archivo de salida")
    parser.add_argument("--force", action="store_true", help="Forzar la regeneración del README sin preguntar")

    args = parser.parse_args()
    generate_readme(args.output)

if __name__ == "__main__":
    main()
