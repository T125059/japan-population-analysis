import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="人口推移分析アプリ", layout="wide")

# タイトルと出典
st.title("都道府県別 人口推移データ分析")
st.caption("出典: [政府統計の総合窓口(e-Stat)](https://www.e-stat.go.jp/dbview?sid=0003448232)より作成")

# データの読み込み
try:
    df = pd.read_csv('data.csv')
    df = df[["都道府県", "西暦", "人口"]]
except Exception as e:
    st.error(f"データの読み込みエラー: {e}")
    st.stop()

# --- サイドバー設定 ---
st.sidebar.header("表示設定")

# 都道府県の選択
all_prefs = df["都道府県"].unique()
selected_prefs = st.sidebar.multiselect(
    "都道府県を選択",
    all_prefs,
    default=["東京都", "大阪府", "北海道"]
)

if not selected_prefs:
    st.warning("左のサイドバーから都道府県を選んでください。")
    st.stop()

# フィルタリング
filtered_df = df[df["都道府県"].isin(selected_prefs)]

# --- 概況表示 ---
st.markdown("### 📊 選択地域の人口概況")

# 最新年と前年のデータを取得して比較
latest_year = filtered_df["西暦"].max()
prev_year = latest_year - 1

latest_data = filtered_df[filtered_df["西暦"] == latest_year]
prev_data = filtered_df[filtered_df["西暦"] == prev_year]

total_pop_latest = latest_data["人口"].sum()
total_pop_prev = prev_data["人口"].sum()
diff = total_pop_latest - total_pop_prev

# メトリクス表示
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(
        label=f"{latest_year}年の総人口 (選択地域計)",
        value=f"{total_pop_latest:,}人",
        delta=f"{diff:,}人"
    )

st.divider()

# --- グラフ描画 ---
col1, col2 = st.columns(2)

# 推移グラフ
with col1:
    st.subheader("推移 (折れ線グラフ)")
    st.line_chart(filtered_df, x="西暦", y="人口", color="都道府県")

# 比較グラフ
with col2:
    st.subheader("最新年の比較 (棒グラフ)")
    st.bar_chart(latest_data, x="都道府県", y="人口", color="都道府県")
    st.write(f"※{latest_year}年時点")

# --- データ詳細とダウンロード ---
with st.expander("データ詳細を確認・ダウンロード"):
    # CSVダウンロード
    csv = filtered_df.to_csv(index=False).encode('utf-8_sig')
    st.download_button(
        label="CSVデータをダウンロード",
        data=csv,
        file_name="population_data.csv",
        mime="text/csv",
    )
    
    # テーブル表示
    st.dataframe(filtered_df.style.format({"人口": "{:,}"}))