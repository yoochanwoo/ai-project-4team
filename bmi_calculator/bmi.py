class BMICalculator:
    def __init__(self, weight, height):
        """
        BMI 계산기 초기화
        :param weight: 체중 (kg)
        :param height: 신장 (cm)
        """
        self.weight = weight
        self.height = height / 100  # cm에서 m로 변환

    def calculate_bmi(self):
        """BMI 계산: 체중(kg) / 신장^2(m)"""
        return self.weight / (self.height ** 2)

    def get_bmi_category(self):
        """BMI 범주 반환"""
        bmi = self.calculate_bmi()
        
        if bmi < 18.5:
            return "저체중"
        elif bmi < 23:
            return "정상"
        elif bmi < 25:
            return "과체중"
        elif bmi < 30:
            return "비만"
        else:
            return "고도비만"

    def get_result(self):
        """BMI 결과 반환"""
        bmi = self.calculate_bmi()
        category = self.get_bmi_category()
        
        return {
            "bmi": round(bmi, 2),
            "category": category
        }