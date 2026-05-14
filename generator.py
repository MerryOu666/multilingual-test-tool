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
