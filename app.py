
import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="KIZASHI", page_icon="🌊", layout="wide")
st.title("KIZASHI")
st.caption("Your Trading Assistant")

file = st.file_uploader("MT4 / MT5のCSVを選択", type=["csv"])

if file:
    raw = file.getvalue()
    text = None
    for enc in ("utf-8-sig", "cp932", "utf-16", "utf-8"):
        try:
            text = raw.decode(enc)
            break
        except:
            pass

    if text is None:
        st.error("CSVを読み込めませんでした。")
    else:
        df = pd.read_csv(io.StringIO(text))
        st.dataframe(df, use_container_width=True)

        profit_col = None
        for c in df.columns:
            if str(c).strip().lower() in ["profit", "損益", "pnl", "net profit"]:
                profit_col = c
                break

        if profit_col is None:
            st.warning("Profit / 損益 / PnL の列が必要です。")
        else:
            p = pd.to_numeric(df[profit_col], errors="coerce").fillna(0)
            wins = p[p > 0]
            losses = p[p < 0]
            gross_profit = wins.sum()
            gross_loss = abs(losses.sum())
            pf = gross_profit / gross_loss if gross_loss else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("合計損益", f"{p.sum():,.0f}")
            c2.metric("勝率", f"{(p>0).mean()*100:.1f}%")
            c3.metric("取引回数", f"{len(p)}")
            c4.metric("PF", f"{pf:.2f}")

            st.line_chart(pd.DataFrame({"累積損益": p.cumsum()}))
            st.info("デモ版：まずは取引履歴の確認から始めます。")
else:
    st.info("同梱の sample_trades.csv を選ぶとすぐ試せます。")
