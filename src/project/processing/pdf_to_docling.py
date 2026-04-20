from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.pipeline_options import PdfPipelineOptions 
from docling.datamodel.base_models import InputFormat   
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from pathlib import Path
import json

pipeline_options = PdfPipelineOptions(
    do_table_structure=True,
    do_cell_matching=False, 
    accelerator_options = AcceleratorOptions(device = AcceleratorDevice.CUDA)
)

convertor = DocumentConverter(  
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend)
    }  
)

source_folder = Path("./data/raw/") # These file paths only work if your terminal is active in the root of the project
output_folder = Path("./data/processed/")

def pdf_export(source: Path, export_fn):
    result = convertor.convert(str(source))

    docling_doc = export_fn(result.document)

    if result.input and result.input._backend:
        result.input._backend.unload()

    return docling_doc

def confirm_overwrite(path: Path) -> bool:
    if not path.exists():
        return True
    
    while True:
        choice = input(f"{path.name} already exists, do you want to overwrite this file? y/n ")

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