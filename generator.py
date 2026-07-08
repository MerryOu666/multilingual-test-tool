import random
from templates import ALL_LANGUAGES

CATEGORY_WEIGHTS = {
    "常规文案": 0.40,
    "长难句": 0.15,
    "短文本": 0.10,
    "数字日期": 0.10,
    "特殊字符": 0.05,
    "边界场景": 0.10,
    "专业术语": 0.05,
    "口语俚语": 0.05,
}

ALL_CATEGORIES = list(CATEGORY_WEIGHTS.keys())

LENGTH_OPTIONS = [100, 500, 1000, 2000]

# 拼接句子时不加空格的语种（无词间空格的书写系统）
NO_SPACE_JOIN_LANGS = {"zh-CN", "ja-JP", "ko-KR", "th-TH"}


def _text_length(text):
    """按可见字符数统计长度（忽略空白符），用于对齐目标字数。"""
    return len("".join(text.split()))


def _join_texts(texts, lang_code):
    sep = "" if lang_code in NO_SPACE_JOIN_LANGS else " "
    return sep.join(texts)


def _trim_to_length(text, target_length):
    if _text_length(text) <= target_length:
        return text

    chars = []
    visible = 0
    for ch in text:
        chars.append(ch)
        if not ch.isspace():
            visible += 1
        if visible >= target_length:
            break
    return "".join(chars).rstrip()


def _generate_one_by_length(mod, pool, lang_code, target_length):
    picked_texts = []
    picked_categories = []
    length_so_far = 0
    # 防止模板极短导致死循环：按字数上限设置最大拼接次数
    max_iterations = target_length * 3 + 50

    for _ in range(max_iterations):
        if length_so_far >= target_length:
            break
        cat, text = random.choice(pool)
        picked_texts.append(text)
        picked_categories.append(cat)
        combined = _join_texts(picked_texts, lang_code)
        length_so_far = _text_length(combined)

    combined = _join_texts(picked_texts, lang_code)
    final_text = _trim_to_length(combined, target_length)

    # 类别标注：若拼接了多个类别，标记为“混合”
    unique_cats = list(dict.fromkeys(picked_categories))
    cat_label = unique_cats[0] if len(unique_cats) == 1 else "混合"

    return {
        "类别": cat_label,
        "语种": mod.LANG_NAME,
        "语种代码": mod.LANG_CODE,
        "目标字数": target_length,
        "实际字数": _text_length(final_text),
        "测试用例": final_text,
    }


def generate_by_length(lang_code, target_length, category="全部", count=1):
    """按目标字数（100/500/1000/2000）拼接模板句子生成 count 条长文本测试用例。"""
    mod = ALL_LANGUAGES.get(lang_code)
    if mod is None:
        return []

    templates = mod.TEMPLATES

    if category != "全部" and category in templates:
        pool = [(category, t) for t in templates[category]]
    else:
        pool = []
        for c in ALL_CATEGORIES:
            if c in templates and templates[c]:
                pool.extend((c, t) for t in templates[c])

    if not pool:
        return []

    results = []
    for idx in range(1, count + 1):
        item = _generate_one_by_length(mod, pool, lang_code, target_length)
        item["序号"] = idx
        results.append(item)
    return results


def generate(lang_code, count, category="全部"):
    mod = ALL_LANGUAGES.get(lang_code)
    if mod is None:
        return []

    templates = mod.TEMPLATES

    if category != "全部" and category in templates:
        pool = [(category, t) for t in templates[category]]
        if len(pool) >= count:
            selected = random.sample(pool, count)
        else:
            selected = pool[:]
            while len(selected) < count:
                selected.append(random.choice(pool))
            random.shuffle(selected)
    else:
        selected = []
        remaining = count
        cats = [c for c in ALL_CATEGORIES if c in templates and templates[c]]
        if not cats:
            return []

        for i, cat in enumerate(cats):
            weight = CATEGORY_WEIGHTS.get(cat, 1.0 / len(cats))
            if i == len(cats) - 1:
                n = remaining
            else:
                n = max(1, round(count * weight))
                n = min(n, remaining)
            remaining -= n

            pool = templates[cat]
            if len(pool) >= n:
                items = random.sample(pool, n)
            else:
                items = pool[:]
                while len(items) < n:
                    items.append(random.choice(pool))
            selected.extend((cat, t) for t in items)

        random.shuffle(selected)

    results = []
    for idx, (cat, text) in enumerate(selected, 1):
        results.append({
            "序号": idx,
            "类别": cat,
            "语种": mod.LANG_NAME,
            "语种代码": mod.LANG_CODE,
            "测试用例": text,
        })
    return results
