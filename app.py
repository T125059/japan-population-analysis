import streamlit as st
import pandas as pd

# ページ設定を行う
st.set_page_config(page_title="人口推移分析アプリ", layout="wide")

# タイトルの表示
st.title("都道府県別 人口推移データ分析")
# 出典元の明記
st.caption("出典: [政府統計の総合窓口(e-Stat)](https://www.e-stat.go.jp/dbview?sid=0003448232)より作成")

# データの読み込み処理
try:
    # Excelで前処理済みのデータを読み込む
    df = pd.read_csv('data.csv')
    
    # 必要な列のみを抽出する（不要な列の排除）
    df = df[["都道府県", "西暦", "人口"]]

except Exception as e:
    # エラー時は停止する
    st.error(f"データの読み込みエラー: {e}")
    st.stop()

# --- サイドバー (条件設定) ---
st.sidebar.header("表示設定")

# 都道府県の選択（複数選択可）
all_prefs = df["都道府県"].unique()
selected_prefs = st.sidebar.multiselect(
    "都道府県を選択",
    all_prefs,
    default=["東京都", "大阪府", "北海道"] # 初期選択値
)

# 選択されていない場合は警告を出して処理を止める
if not selected_prefs:
    st.warning("左のサイドバーから都道府県を選んでください。")
    st.stop()

# データのフィルタリングを実行
filtered_df = df[df["都道府県"].isin(selected_prefs)]

# 【未使用UI 2】区切り線を表示
st.divider()

# --- グラフ描画 ---
# カラムを2つに分割してレイアウトする
col1, col2 = st.columns(2)

with col1:
    st.subheader("推移 (折れ線グラフ)")
    st.line_chart(filtered_df, x="西暦", y="人口", color="都道府県")

with col2:
    st.subheader("最新年の比較 (棒グラフ)")
    # データの中で最も新しい年を自動取得する
    latest_year = filtered_df["西暦"].max()
    latest_df = filtered_df[filtered_df["西暦"] == latest_year]
    
    # 棒グラフの描画
    st.bar_chart(latest_df, x="都道府県", y="人口", color="都道府県")
    st.write(f"※{latest_year}年時点")

# 【未使用UI 3】データ詳細を折りたたみ表示にする
with st.expander("データ詳細を確認する"):
    st.dataframe(filtered_df)