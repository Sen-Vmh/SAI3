from docling.document_converter import DocumentConverter
import os
from pathlib import Path
import json

source_folder = Path("./data/raw/") # These file paths only work if your terminal is active in the root of the project.
output_folder = Path("./data/processed/")

convertor = DocumentConverter()
    
def pdf_to_docling(source: Path):
    return convertor.convert(str(source)).document

def pdf_export(source: Path, export_fn):
    doc = pdf_to_docling(source)

    return export_fn(doc)

def confirm_overwrite(path: Path) -> bool:
    if not path.exists():
        return True
    
    while True:
        choice = input(f"{file_path.name} already exists, do you want to overwrite this file? y/n")

        if choice == "y":
            return True  
        elif choice == "n":
            print("Skipping file.")
            return False
        else:
            print("Please enter 'y' or 'n'.")

for file_path in Path.iterdir(source_folder):
    if file_path.name == "data_files.md": 
        continue
    
    output_file = output_folder / "json" / (file_path.stem + ".json")

    print(f"loading file {file_path.stem} at {output_file}")

    if not confirm_overwrite(output_file):
        continue        

    json_data = pdf_export(file_path, lambda d: d.export_to_dict())
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=2)