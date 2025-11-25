import streamlit as st
import pandas as pd
import numpy as np

# ================================
# マスターデータ：カテゴリ / 業界 / サービス
# ================================
industries_by_category = {
    "BtoC": [
        "教育業界（予備校・塾・オンライン学習）",
        "飲食業界（レストラン・カフェ）",
        "美容・コスメ業界",
        "アパレル・ファッション業界",
        "旅行・観光業界",
        "エンタメ・ゲーム業界",
        "フィットネス・ヘルスケア（個人向け）",
    ],
    "BtoB": [
        "IT・SaaS業界（法人向けツール）",
        "人材・採用支援業界",
        "コンサルティング業界",
        "物流・サプライチェーン業界",
        "製造業（部品・機械など）",
        "法人向け教育・研修業界",
    ],
    "BtoG": [
        "公共教育（学校・自治体向けサービス）",
        "医療・福祉（病院・行政向け）",
        "インフラ（電気・ガス・交通）",
        "行政DX・自治体向けIT",
    ],
}

service_options_by_industry = {
    "教育業界（予備校・塾・オンライン学習）": [
        "オンライン自習室",
        "動画学習サブスク",
        "英会話アプリ",
        "資格対策プラットフォーム",
    ],
    "飲食業界（レストラン・カフェ）": [
        "モバイルオーダーアプリ",
        "予約管理システム",
        "テイクアウト注文アプリ",
    ],
    "美容・コスメ業界": [
        "美容予約アプリ",
        "コスメサブスクBOX",
        "オンライン肌診断サービス",
    ],
    "アパレル・ファッション業界": [
        "ECサイト（ファッション通販）",
        "コーディネート提案アプリ",
        "サブスクレンタルサービス",
    ],
    "旅行・観光業界": [
        "旅行予約プラットフォーム",
        "観光ガイドアプリ",
    ],
    "エンタメ・ゲーム業界": [
        "動画配信サービス",
        "音楽ストリーミング",
        "ゲーム課金プラットフォーム",
    ],
    "フィットネス・ヘルスケア（個人向け）": [
        "オンラインフィットネス",
        "ヘルスケア記録アプリ",
    ],
    "IT・SaaS業界（法人向けツール）": [
        "営業支援SaaS（SFA）",
        "顧客管理システム（CRM）",
        "社内チャットツール",
    ],
    "人材・採用支援業界": [
        "求人掲載プラットフォーム",
        "採用管理システム（ATS）",
    ],
    "コンサルティング業界": [
        "オンライン診断フォーム",
        "研修管理プラットフォーム",
    ],
    "物流・サプライチェーン業界": [
        "在庫管理システム",
        "配送ルート最適化ツール",
    ],
    "製造業（部品・機械など）": [
        "生産管理システム",
        "IoT機器モニタリング",
    ],
    "法人向け教育・研修業界": [
        "eラーニングプラットフォーム",
        "社内研修管理システム",
    ],
    "公共教育（学校・自治体向けサービス）": [
        "学習eポータル",
        "校務支援システム",
        "保護者連絡アプリ",
    ],
    "医療・福祉（病院・行政向け）": [
        "電子カルテ連携システム",
        "オンライン診療基盤",
        "福祉サービス管理システム",
    ],
    "インフラ（電気・ガス・交通）": [
        "利用者ポータルサイト",
        "スマートメーター管理",
        "交通運行管理システム",
    ],
    "行政DX・自治体向けIT": [
        "オンライン申請システム",
        "住民ポータル",
        "庁内文書管理システム",
    ],
}

def init_session_state():
    defaults = {
        "category": "BtoC",
        "industry": industries_by_category["BtoC"][0],
        "service": "オンライン自習室",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def main():
    init_session_state()

    st.set_page_config(
        page_title="意思決定サポート統計アプリ｜企画書ジェネレーター",
        layout="wide",
    )

    st.title("意思決定サポート統計アプリ｜企画書ジェネレーター")
    st.caption("Problem → Affinity → Solution → Offer → Narrowing Down → Action → First Action → Closing")

    # ------------------------------
    # 分析対象設定（全タブ共通）
    # ------------------------------
    with st.expander("分析対象の設定（全タブ共通）", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            category = st.radio(
                "カテゴリ",
                ["BtoC", "BtoB", "BtoG"],
                index=["BtoC", "BtoB", "BtoG"].index(st.session_state["category"]),
                format_func=lambda x: {
                    "BtoC": "BtoC（一般消費者向け）",
                    "BtoB": "BtoB（企業向け）",
                    "BtoG": "BtoG・公共系",
                }[x],
            )
        industries = industries_by_category[category]
        with c2:
            industry = st.selectbox(
                "業界",
                industries,
                index=industries.index(st.session_state.get("industry", industries[0])),
            )
        services = service_options_by_industry.get(industry, ["サービス例なし"])
        with c3:
            current_service = st.session_state.get("service")
            idx = services.index(current_service) if current_service in services else 0
            service = st.selectbox("サービス", services, index=idx)

        st.session_state["category"] = category
        st.session_state["industry"] = industry
        st.session_state["service"] = service

        st.markdown(f"**分析対象：** {category} / {industry} / {service}")

    # ------------------------------
    # タブ定義
    # ------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "1. Problem（外部分析）",
        "2. Affinity（顧客分析）",
        "3. Solution（データ基盤）",
        "4. Offer（競合分析）",
        "5. Narrowing Down（効果分析）",
        "6. Action（成長戦略）",
        "7. First Action（KPI設計）",
        "8. Closing（統合レポート）",
    ])

    # ========== タブ1：Problem ==========
    with tab1:
        st.header("1. Problem｜外部分析（市場・環境の“不確実性”）")
        st.markdown("**ロールプレイング**：総務省/厚生労働省/Googleトレンドで市場調査しといて〜、と急に振られた。")
        st.markdown("**悩み**：優先順位がつかない！どこまでどのくらい調べたらいいの？")

        st.subheader("調査項目リスト")
        default_items = "市場規模\n成長率\n競合数\n検索ボリューム"
        items_text = st.text_area("調べたい項目を1行ずつ入力", default_items)
        items = [line.strip() for line in items_text.splitlines() if line.strip()]
        if items:
            weights = []
            st.write("各項目の“重要度”を0〜10でざっくり入力してください。")
            for item in items:
                w = st.slider(item, 0, 10, 5)
                weights.append(w)
            df = pd.DataFrame({"項目": items, "重要度": weights})
            st.subheader("重要度一覧")
            st.dataframe(df, use_container_width=True)
            st.subheader("重要度の棒グラフ")
            st.bar_chart(df.set_index("項目"))

    # ========== タブ2：Affinity ==========
    with tab2:
        st.header("2. Affinity｜顧客分析（“誰”の“どんな悩み”か）")
        st.markdown("**ロールプレイング**：新規サービスの顧客シミュレーションで、想定ベネフィット作っておいて〜と言われた。")
        st.markdown("**悩み**：このデータほんとにあってる？“どんな人がどれくらい”いるのか、感覚じゃなくて分布で見たい！")

        st.subheader("簡易ペルソナ分布シミュレーション")
        n = st.slider("サンプル人数（ダミーデータ）", 50, 500, 200, 50)
        ages = np.random.normal(loc=30, scale=8, size=n).astype(int)
        ages = np.clip(ages, 15, 65)
        persona_df = pd.DataFrame({"年齢": ages})
        st.write("ダミーの年齢分布データ（簡易）")
        st.dataframe(persona_df.head(), use_container_width=True)
        st.subheader("年齢ヒストグラム")
        hist = persona_df["年齢"].value_counts().sort_index()
        st.bar_chart(hist)

    # ========== タブ3：Solution ==========
    with tab3:
        st.header("3. Solution｜データ基盤（GIGOを防ぐ設計）")
        st.markdown("**ロールプレイング**：新規アンケートと既存データ、フォームとデータを整理してと言われた。")
        st.markdown("**悩み**：型がバラバラ＆抜けだらけで集計できない…")

        st.subheader("サンプルデータ（型の違いと欠損）")
        raw_df = pd.DataFrame({
            "年齢": [25, "30", None, 22, "不明"],
            "購入回数": ["1", "2", "3", None, "5"],
        })
        st.dataframe(raw_df, use_container_width=True)

        st.subheader("簡易クレンジング結果（年齢・購入回数を数値化）")
        clean_df = raw_df.copy()
        clean_df["年齢"] = pd.to_numeric(clean_df["年齢"], errors="coerce")
        clean_df["購入回数"] = pd.to_numeric(clean_df["購入回数"], errors="coerce")
        clean_df = clean_df.dropna()
        st.dataframe(clean_df, use_container_width=True)

    # ========== タブ4：Offer ==========
    with tab4:
        st.header("4. Offer｜競合分析（差別化提案の根拠）")
        st.markdown("**ロールプレイング**：新規サービスのポジションを決めたいから、競合比較してと言われた。")

        st.subheader("競合2社の“品質スコア”ダミーデータ")
        size = st.slider("サンプル数（品質スコア）", 10, 200, 50, 10)
        np.random.seed(0)
        a = np.random.normal(loc=70, scale=10, size=size)
        b = np.random.normal(loc=75, scale=15, size=size)
        comp_df = pd.DataFrame({"競合A": a, "競合B": b})
        st.dataframe(comp_df.head(), use_container_width=True)

        st.subheader("分散（ばらつき）の比較（F検定のイメージ）")
        var_a = np.var(a, ddof=1)
        var_b = np.var(b, ddof=1)
        st.write(f"競合Aの分散：{var_a:.2f}")
        st.write(f"競合Bの分散：{var_b:.2f}")

    # ========== タブ5：Narrowing Down ==========
    with tab5:
        st.header("5. Narrowing Down｜効果分析（施策の“効き”を絞り込む）")
        st.markdown("**ロールプレイング**：イベント施策、本当に効いたのか検証したいと言われた。")

        st.subheader("施策A/Bの売上ダミーデータ")
        size2 = st.slider("サンプル数（施策ごと）", 10, 200, 40, 10)
        np.random.seed(1)
        a_sales = np.random.normal(loc=100, scale=20, size=size2)
        b_sales = np.random.normal(loc=110, scale=25, size=size2)
        ab_df = pd.DataFrame({"施策A": a_sales, "施策B": b_sales})
        st.dataframe(ab_df.head(), use_container_width=True)

        st.subheader("平均の比較（T検定イメージ）")
        mean_a = a_sales.mean()
        mean_b = b_sales.mean()
        diff = mean_b - mean_a
        st.write(f"施策Aの平均：{mean_a:.1f}")
        st.write(f"施策Bの平均：{mean_b:.1f}")
        st.write(f"平均差（B - A）：{diff:.1f}")

    # ========== タブ6：Action ==========
    with tab6:
        st.header("6. Action｜成長戦略（KGI/KPIと時系列）")
        st.markdown("**ロールプレイング**：新規サービスの成長戦略を描いてと言われた。")

        st.subheader("売上の時系列ダミーデータ")
        periods = st.slider("期間（月数）", 6, 36, 12, 6)
        np.random.seed(2)
        trend = np.linspace(80, 150, periods)
        noise = np.random.normal(scale=5, size=periods)
        sales_ts = trend + noise
        ts_df = pd.DataFrame({"月": list(range(1, periods + 1)), "売上指数": sales_ts})
        ts_df = ts_df.set_index("月")
        st.line_chart(ts_df)

    # ========== タブ7：First Action ==========
    with tab7:
        st.header("7. First Action｜KPI設計（最初の一歩を数値に落とす）")
        st.markdown("**ロールプレイング**：KPI出して、と言われたけれど何から決めればいいか分からない。")

        st.subheader("KPI候補の書き出し")
        default_kpis = "月間アクティブユーザー\n新規登録数\n継続率"
        kpi_text = st.text_area(
            "KPI候補を1行ずつ入力（例：月間アクティブユーザー、CV数、継続率など）",
            default_kpis,
        )
        kpis = [line.strip() for line in kpi_text.splitlines() if line.strip()]
        if kpis:
            st.write("KPIツリーの“葉っぱ”候補：")
            for k in kpis:
                st.markdown(f"- {k}")

    # ========== タブ8：Closing ==========
    with tab8:
        st.header("8. Closing｜統合レポート（企画書としてまとめる）")
        st.markdown("これまで入力・シミュレーションしてきた内容を、企画書の構成に並べるイメージです。")

        outline = [
            "1. Problem：市場の不確実性と背景",
            "2. Affinity：ターゲット像と顧客インサイト",
            "3. Solution：データ基盤と記録設計",
            "4. Offer：競合比較とポジショニング",
            "5. Narrowing Down：施策効果と学び",
            "6. Action：成長シナリオとKGI/KPI",
            "7. First Action：直近3ヶ月の実行プラン",
            "8. Closing：まとめとNext Action / 依頼事項",
        ]
        st.subheader("企画書アウトライン（サンプル）")
        st.markdown("- " + "\n- ".join(outline))

if __name__ == "__main__":
    main()
