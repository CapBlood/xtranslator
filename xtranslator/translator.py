from argostranslate import package, translate


def get_translator(path):
    package.install_from_path(path)
    installed_languages = translate.load_installed_languages()
    translation_en_es = installed_languages[0].get_translation(installed_languages[1])

    def translate_english(to_translate):
        return translation_en_es.translate(to_translate)

    return translate_english