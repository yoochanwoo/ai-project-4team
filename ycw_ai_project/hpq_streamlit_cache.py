import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib # 머신러닝 내용을 저장하고, 재호출시에 사용
import streamlit as st

# 데이터 준비
@st.cache_data # 함수의 입력 매개변수와 반환 값을 캐시에 저장하여 호출 시 재사용
def load_data():
    hpq_data = pd.read_csv('dataset/HeartPredictionQuantumDataset.csv', encoding='cp949')

    X = hpq_data.iloc[:,:-1].values
    #print(X)
    y = hpq_data.iloc[:,-1].values
    #print(y)

    XColumns = list(hpq_data.columns[:-1])

    # 스케일링 처리
    # 데이터 프레임으로 변환
    Xdf = pd.DataFrame(X, columns = XColumns)     
    #print(Xdf)

    # 데이터 전처리: 특성 스케일링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(Xdf)
    X_scaled = pd.DataFrame(X_scaled, columns=Xdf.columns)

    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 머신러닝 모델
    ## 랜덤포레스트
    rf_model = RandomForestClassifier(random_state=42, n_estimators=100) # n_esimators : 모델을 구성하는 결정 틀의 개수수
    # Random Forest 모델 생성
    # 하이퍼파라미터 튜닝을 위해 GridSearchCV 사용
    param_grid = {
        'n_estimators': [50, 100, 200],  # 트리의 개수
        'max_depth': [4, 6, 8],       # 트리의 최대 깊이
        'min_samples_split': [2, 4],  # 노드를 분할하기 위한 최소 샘플 수
        'min_samples_leaf': [1, 2]    # 리프 노드에 있어야 하는 최소 샘플 수
    }
    # 교차 검증 cv =3 : 훈련 데이터를 3개의 FOLD(묶음)으로 나누어서 두개를 훈련, 나머지는 검증 용도로 활용
    # 교차 검증은 최적의 하이퍼 파라미터 값을 찾기 위해서 사용됨
    grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='accuracy')

    # 학습
    ## 랜덤포레스트
    # 모델 학습 (GridSearchCV를 통한 최적의 파라미터를 반영한 학습)
    grid_search.fit(X_train, y_train)
    # 최적의 모델 저장
    best_rf_model = grid_search.best_estimator_
    rf_y_pred = best_rf_model.predict(X_test)

    # 평가
    rf_accuracy = accuracy_score(y_test, rf_y_pred) # 정확도 계산
    print(f"Accuracy: {rf_accuracy:.4f}") # 결과 출력 : 1.0000
    print("\nClassification Report:\n", classification_report(y_test, rf_y_pred))

    # 모델 저장
    joblib.dump(best_rf_model, 'hpq.pkl')

    # 교차 검증 수행
    cv_scores = cross_val_score(best_rf_model, X, y, cv=5)
    print(f"평균 정확도: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # 특성 중요도 계산
    feature_importance = pd.DataFrame({
        '특성': XColumns,
        '중요도': best_rf_model.feature_importances_
    }).sort_values('중요도', ascending=False)

    # 특성 중요도 시각화
    ## 폰트지정
    plt.rcParams['font.family'] = 'Malgun Gothic'
    ## 마이너스 부호 깨짐 지정
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots()
    ax.set_title('특성 중요도')
    sns.barplot(x='중요도', y='특성', data=feature_importance, ax=ax)
    st.pyplot(fig)
    
    return best_rf_model

best_rf_model = load_data()

# 4. streamlit UI 구현
st.title("심장질환 여부 예측 시스템 구현")
st.write('값을 입력하여 심장질환 여부를 예측해보세요.')

# 사용자 입력받기
age = st.slider('나이 (년)', min_value=20, max_value=90, value=55, step=1)
gender = st.slider('성별 (0:여성, 1:남성)', min_value=0, max_value=1, value=0, step=1)
blood_pressure = st.slider('혈압', min_value=80, max_value=200, value=140, step=1)
cholesterol = st.slider('콜레스테롤', min_value=150, max_value=300, value=225, step=1)
heart_rate = st.slider('분당심박수', min_value=60, max_value=120, value=90, step=1)
quantum_pattern_feature = st.slider('모델구분값', min_value=6.00, max_value=11.00, value=8.50, step=0.01)

# 예측하기 버튼
if st.button('예측하기'):
    # 입력값을 모델에 전달
    model = joblib.load('hpq.pkl')
    input_data = np.array([[age, gender, blood_pressure, cholesterol,
                           heart_rate, quantum_pattern_feature]])
    prediction = model.predict(input_data)[0]

    # 결과 출력
    if prediction == 0:
        st.write('예측 결과: 심장질환 없음.')
    elif prediction == 1:
        st.write('예측 결과: 심장질환 있음.')
    else:
        st.write('예측 불가')
