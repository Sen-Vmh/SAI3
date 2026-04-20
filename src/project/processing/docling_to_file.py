from pathlib import Path

from docling.document_converter import DocumentConverter

source_folder = Path("./data/processed/") # These file paths only work if your terminal is active in the root of the project
output_folder = Path("./data/processed/")

converter = DocumentConverter()

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