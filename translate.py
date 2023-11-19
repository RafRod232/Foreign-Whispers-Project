import argostranslate.package
import argostranslate.translate

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


translatedText = translate_captions_file("captions/Bill Gates_ The 2021 60 Minutes interview.srt", "en", "ko")
print(translatedText)