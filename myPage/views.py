from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser, Company, Booth, BoothQueue

class MyPageView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, userId):
        # 사용자 정보 가져오기
        user = get_object_or_404(CustomUser, id=userId)

        # 관심 있는 회사 가져오기
        interested_companies = [
            {"name": company.name, "promotional_content": company.promotional_content}
            for company in user.interested_companies.all()
        ]

        # 참여했던 부스 가져오기
        participated_booths = [
            {
                "booth_id": booth.booth_id,
                "company_name": booth.company.name,
                "day": booth.day,
                "floor": booth.floor,
                "boothNum": booth.boothNum,
                "boothCate": booth.boothCate,
                "boothName": booth.boothName,
            }
            for booth in user.participated_booths.all()
        ]

        # 사용자 정보를 JSON 형식으로 반환
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phoneNum": user.phoneNum,
            "birth": user.birth,
            "age": user.age,
            "school": user.school,
            "department": user.department,
            "admission_date": user.admission_date,
            "graduation_date": user.graduation_date,
            "experience": user.experience,
            "self_introduction": user.self_introduction,
            "companies_of_interest": user.companies_of_interest,
            "interested_companies": interested_companies,
            "participated_booths": participated_booths,
        }
        return JsonResponse(user_data)
