import streamlit as st
import pandas as pd
from generator import generate, generate_by_length, ALL_CATEGORIES, LENGTH_OPTIONS
from exporter import to_excel_bytes, to_csv_bytes, make_filename
from templates import get_language_options

st.set_page_config(page_title="多语种测试用例生成工具", page_icon="🌐", layout="wide")

st.markdown(
    """
    <style>
    .main-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1rem; color: #666; margin-bottom: 1.5rem; }
    .stDataFrame { font-size: 14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🌐 多语种测试用例生成工具</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">按语种一键批量生成原生测试用例，支持导出 Excel / CSV</div>',
    unsafe_allow_html=True,
)

lang_options = get_language_options()
lang_display = {code: f"{name} ({code})" for code, name in lang_options.items()}

gen_mode = st.radio(
    "生成模式",
    options=["按数量生成", "按字数生成"],
    horizontal=True,
)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_lang = st.selectbox(
        "选择语种",
        options=list(lang_display.keys()),
        format_func=lambda x: lang_display[x],
    )

with col2:
    if gen_mode == "按数量生成":
        count = st.number_input("生成数量", min_value=1, max_value=500, value=20, step=5)
    else:
        target_length = st.selectbox(
            "目标字数",
            options=LENGTH_OPTIONS,
            index=1,
            format_func=lambda n: f"{n} 字",
        )

with col3:
    category_options = ["全部"] + ALL_CATEGORIES
    selected_category = st.selectbox("用例类别", options=category_options)

generate_btn = st.button("🚀 生成用例", type="primary", use_container_width=True)

if generate_btn:
    with st.spinner("正在生成测试用例..."):
        if gen_mode == "按数量生成":
            results = generate(selected_lang, count, selected_category)
        else:
            results = generate_by_length(selected_lang, target_length, selected_category)

    if not results:
        st.warning("未找到该语种的模板数据，请检查配置。")
    else:
        st.session_state["results"] = results
        st.session_state["lang_name"] = lang_options[selected_lang]

if "results" in st.session_state and st.session_state["results"]:
    results = st.session_state["results"]
    lang_name = st.session_state["lang_name"]

    st.success(f"✅ 已生成 **{len(results)}** 条 **{lang_name}** 测试用例")

    df = pd.DataFrame(results)
    display_cols = [c for c in ["序号", "类别", "目标字数", "实际字数", "测试用例"] if c in df.columns]
    st.dataframe(
        df[display_cols],
        use_container_width=True,
        height=min(len(results) * 40 + 40, 600),
        hide_index=True,
    )

    col_a, col_b, _ = st.columns([1, 1, 3])

    with col_a:
        excel_data = to_excel_bytes(results, lang_name)
        st.download_button(
            label="📥 导出 Excel",
            data=excel_data,
            file_name=make_filename(lang_name, "xlsx"),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col_b:
        csv_data = to_csv_bytes(results)
        st.download_button(
            label="📥 导出 CSV",
            data=csv_data,
            file_name=make_filename(lang_name, "csv"),
            mime="text/csv",
            use_container_width=True,
        )
