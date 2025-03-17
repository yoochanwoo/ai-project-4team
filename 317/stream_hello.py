import streamlit as st

st.title('Hello Streamlit!')

"""
1. 페이지 구성
    st.title() : 페이지 제목 설정

    st.header() : 페이지 헤더 설정
    st.subheader() : 페이지 서브헤더 설정
    
    st,tabs() : 탭의 이름을 리스트 형태로 받아서 설정

2. 데이터 표시
    st.write() : 다양한 형태의 데이터를 출력
    st.dataframe() : 데이터프레임을 출력
    st.table() : 정적 테이블을 출력

3. 대화형 위젯
    st.slider() : 슬라이더를 통해 값을 선택
    st.selectbox() : 드롭다운 리스트를 통해 값을 선택
    st.button() : 버튼을 통해 이벤트 처리
    st.checkbox() : 체크박스를 통해 값을 선택
    st.radio() : 라디오 버튼을 통해 값을 선택
    st.text_input() : 텍스트를 입력
    st.text_area() : 여러 줄의 텍스트를 입력
    st.date_input() : 날짜를 입력
    st.time_input() : 시간을 입력
    st.file_uploader() : 파일을 업로드
    
4. 시각화
    st.pyplot() : matplotlib으로 그린 그래프를 출력
    st.altair_chart() : Altair로 그린 그래프를 출력
    st.bokeh_chart() : Bokeh로 그린 그래프를 출력
    st.vega_lite_chart() : Vega-Lite로 그린 그래프를 출력
    st.plotly_chart() : Plotly로 그린 그래프를 출력
    st.bar_chart() : 막대 그래프를 출력
    st.line_chart() : 선 그래프를 출력
    st.map() : 지도를 출력    

5. 레이아웃
    st.sidebar() : 사이드바에 위젯을 배치
    st.columns() : 여러 열로 위젯을 배치
    st.expander() : 접혀진 상태로 위젯을 배치
    st.beta_container() : 베타 컨테이너를 생성
    st.beta_columns() : 베타 컬럼을 생성
    st.beta_expander() : 베타 확장자를 생성
"""