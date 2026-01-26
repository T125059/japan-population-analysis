import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="人口推移分析アプリ", layout="wide")

# タイトル
st.title("都道府県別 人口推移データ分析")
# 【未使用UI 1】 st.caption
st.caption("出典: 政府統計の総合窓口(e-Stat)より作成")

# データの読み込み
try:
    # アップロードされたdata.csvを読み込む
    df = pd.read_csv('data.csv')
except Exception as e:
    st.error(f"データの読み込みエラー: {e}")
    st.stop()

# --- サイドバー (条件設定) ---
st.sidebar.header("表示設定")

# 都道府県選択
all_prefs = df["都道府県"].unique()
selected_prefs = st.sidebar.multiselect(
    "都道府県を選択",
    all_prefs,
    default=["東京都", "大阪府", "北海道"] # 初期選択
)

if not selected_prefs:
    st.warning("左のサイドバーから都道府県を選んでください。")
    st.stop()

# フィルタリング
filtered_df = df[df["都道府県"].isin(selected_prefs)]

# 【未使用UI 2】 st.divider
st.divider()

# --- グラフ描画 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("人口推移 (折れ線グラフ)")
    st.line_chart(filtered_df, x="西暦", y="人口", color="都道府県")

with col2:
    st.subheader("最新年の比較 (棒グラフ)")
    # データの中で一番新しい年を自動取得
    latest_year = filtered_df["西暦"].max()
    latest_df = filtered_df[filtered_df["西暦"] == latest_year]
    
    st.bar_chart(latest_df, x="都道府県", y="人口", color="都道府県")
    st.write(f"※{latest_year}年時点")

# 【未使用UI 3】 st.expander
with st.expander("データ詳細を確認する"):
    st.dataframe(filtered_df)