import streamlit as st
import pandas as pd

st.set_page_config(page_title="무료 와이파이 찾아드림료", layout="wide")

st.title("📍 무료 와이파이 찾아드림료")
st.write("원하는 지역의 무료 와이파이 위치를 찾아보세요!")

# CSV 파일 로드
@st.cache_data
def load_wifi_data():
    try:
        df = pd.read_csv("공공와이파이.csv", encoding="utf-8", on_bad_lines="skip")
    except:
        df = pd.read_csv("공공와이파이.csv", encoding="cp949", on_bad_lines="skip")

    df.columns = ["시도", "시군구", "읍면동", "위치명", "위도", "경도"]
    return df

df = load_wifi_data()

# 사이드바에서 지역 선택
st.sidebar.header("🔍 지역 검색")

# 시도 선택
provinces = sorted(df["시도"].unique())
selected_province = st.sidebar.selectbox("시/도 선택", provinces)

# 선택된 시도로 필터링
df_filtered = df[df["시도"] == selected_province]
districts = sorted(df_filtered["시군구"].unique())
selected_district = st.sidebar.selectbox("시/군/구 선택", districts)

# 선택된 시도, 시군구로 필터링
df_filtered2 = df_filtered[df_filtered["시군구"] == selected_district]
dongs = sorted(df_filtered2["읍면동"].unique())
selected_dong = st.sidebar.selectbox("읍/면/동 선택", dongs)

# 찾기 버튼
if st.sidebar.button("🔍 찾기", use_container_width=True):
    # 최종 필터링
    result_df = df_filtered2[df_filtered2["읍면동"] == selected_dong]

    if len(result_df) > 0:
        st.success(f"✅ {selected_province} {selected_district} {selected_dong}에서 {len(result_df)}개의 무료 와이파이를 찾았습니다!")

        # 테이블로 표시
        st.subheader("📋 무료 와이파이 목록")
        display_df = result_df[["위치명", "위도", "경도"]].reset_index(drop=True)
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)

        # 지도 표시
        st.subheader("🗺️ 위치 지도")
        st.map(result_df[["위도", "경도"]])
    else:
        st.warning("⚠️ 선택한 지역에서 무료 와이파이를 찾을 수 없습니다.")
