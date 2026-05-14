from . import zh_CN, en_GB, th_TH, vi_VN, ko_KR, fr_FR, ja_JP, es_ES, ar_SA, ru_RU, pt_BR, de_DE, fil_PH, ms_MY, id_ID

ALL_LANGUAGES = {
    "zh-CN": zh_CN,
    "en-GB": en_GB,
    "th-TH": th_TH,
    "vi-VN": vi_VN,
    "ko-KR": ko_KR,
    "fr-FR": fr_FR,
    "ja-JP": ja_JP,
    "es-ES": es_ES,
    "ar-SA": ar_SA,
    "ru-RU": ru_RU,
    "pt-BR": pt_BR,
    "de-DE": de_DE,
    "fil-PH": fil_PH,
    "ms-MY": ms_MY,
    "id-ID": id_ID,
}

def get_language_options():
    return {code: mod.LANG_NAME for code, mod in ALL_LANGUAGES.items()}

def get_templates(lang_code):
    mod = ALL_LANGUAGES.get(lang_code)
    if mod is None:
        return {}
    return mod.TEMPLATES
