import argostranslate.package
import argostranslate.translate
import os

# from_code and to_code are language codes:
def translate_text(text, from_code, to_code):
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    return argostranslate.translate.translate(text, from_code, to_code)

def translate_captions_file(file_path, from_code, to_code):
    captions_file = open(file_path, "r")
    captions_text = captions_file.read()
    captions_file.close()
    return translate_text(captions_text, from_code, to_code)

def translate_captions_folder(folder_path, from_code, to_code, output_folder):
    translated_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            translated_text = translate_captions_file(file_path, from_code, to_code)
            translated_texts[filename] = translated_text
            output_file_path = os.path.join(output_folder, f"{filename.split('.')[0]}_french_translated.txt")
            with open(output_file_path, "w") as output_file:
                output_file.write(translated_text)

    return translated_texts
os.makedirs("french_captions", exist_ok=True)
translated_texts = translate_captions_folder("whisper_captions", "en", "fr", "french_captions")
