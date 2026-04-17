from docling.document_converter import DocumentConverter
import os
from pathlib import Path

source_folder = Path("./data/raw/") # These file paths only work if your terminal is active in the root of the project.
output_folder = Path("./data/processed/")

def pdf_to_docling(source: Path) -> str:
    convertor = DocumentConverter()
    return convertor.convert(str(source)).document
    

def pdf_export(source: Path, export_fn):
    doc = pdf_to_docling(source)

    return export_fn(doc)



for file_path in Path.iterdir(source_folder):
    if file_path.name == "data_files.md": 
        continue
    
    output_file = output_folder / (file_path.stem + ".txt")
    
    with open(output_file, "w") as file:
        file.write(file_path.stem + ".txt")