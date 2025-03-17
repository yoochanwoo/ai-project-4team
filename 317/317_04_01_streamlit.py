import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib # 머신러닝 내용을 저장하고, 재호출시에 사용
import streamlit as st

# 1. 데이터 준비 , 2. 특성 선택
data = pd.read_csv('./dataset/HR_comma_sep.csv', encoding='cp949')

X = data[['satisfaction_level', 'number_project', 'time_spend_company']]
y = data['left']

# 3. 모델 선택 및 학습
# 데이터 전처리: 특성 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 모델 저장
joblib.dump(rf_model, 'HR_comma_sep_model.pkl')

# 테스트 데이터로 정확도 확인
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# 교차 검증 수행
cv_scores = cross_val_score(rf_model, X_scaled, y, cv=5)

# 특성 중요도 계산
feature_importance = pd.DataFrame({
    '특성': X.columns,
    '중요도': rf_model.feature_importances_
}).sort_values('중요도', ascending=False)

# 결과 출력
print("모델 성능 평가:")
print("\n교차 검증 점수:")
print(f"평균 정확도: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
print("\n분류 리포트:")
print(classification_report(y_test, y_pred))

# 특성 중요도 시각화
plt.figure(figsize=(10, 6))
sns.barplot(x='중요도', y='특성', data=feature_importance)
plt.title('특성 중요도')
plt.show()

# 4. streamlit UI 구현
st.title("퇴사 여부 예측 시스템 구현")
st.write('값을 입력하여 퇴사 여부를 예측해보세요.')

# 사용자 입력받기
satisfaction_level = st.slider('Satisfaction (만족도)', min_value=0.00, max_value=1.00, value=0.50, step=0.01)
number_project = st.slider('Project (프로젝트 수)', min_value=1, max_value=10, value=5)
time_spend_company = st.slider('Time Spend (근무 연수)', min_value=1, max_value=20, value=10)

# 예측하기 버튼
if st.button('예측하기'):
    # 입력값을 모델에 전달
    model = joblib.load('HR_comma_sep_model.pkl')
    input_data = np.array([[satisfaction_level, number_project, time_spend_company]])
    prediction = model.predict(input_data)[0]

    # 결과 출력
    if prediction == 1:
        st.write('예측 결과: 퇴사 가능성이 높습니다.')
    else:
        st.write('예측 결과: 퇴사 가능성이 낮습니다.')
        
# 5. 데이터 효율성
@st.cache_data # 함수의 입력 매개변수와 반환 값을 캐시에 저장하여 호출 시 재사용
def load_data():
    data = pd.read_csv('dataset/HR_comma_sep.csv', encoding='cp949')
    data.rename(columns={'Departments ': 'Departments'}, inplace=True)
    data = pd.get_dummies(data, columns=['Departments', 'salary'], drop_first=True)
    return data