from docling.document_converter import DocumentConverter
from pathlib import Path
import json

from src.utils import confirm_overwrite

convertor = DocumentConverter()

source_folder = Path("./data/processed/json") # These file paths only work if your terminal is active in the root of the project
output_folder = Path("./data/processed/")

export_file_type = "text"

while True:
    export_file_type = input("Choose what file you type you want to export your docling document to: \n1. text\n2. markdown\n3. json")
    
    if export_file_type == "1":
        export_file_type = "text"
        break
    elif export_file_type == "2":
        export_file_type = "markdown"
        break
    elif export_file_type == "3":
        export_file_type = "json"
        break
    else:        
        print("Please enter a valid option (1, 2, or 3).")

export_dict = {
    "text": lambda d: d.export_to_text(),
    "markdown": lambda d: d.export_to_markdown(),
    "json": lambda d: d.export_to_dict()
}

def export_to_file(source: Path, export_fn):# -> Any:
    result = convertor.convert(str(source))

    docling_doc = export_fn(result.document)

    return docling_doc

for file_path in Path.iterdir(source_folder):    
    output_file = output_folder / export_file_type / (file_path.stem + f".{export_file_type}")

    print(f"loading file {file_path.stem} at {output_file}")

    if not confirm_overwrite(output_file):
        continue        

    json_data = export_to_file(file_path, export_dict[export_file_type])
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=2)