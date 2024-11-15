from django.http import JsonResponse
from django.views import View
from users.models import InterestCategory, CustomUser, Company, Booth, BoothQueue
from django.core.serializers import serialize
import json

from django.http import JsonResponse
from rest_framework.views import APIView


class AllDataView(APIView):
    def get(self, request):
        data_structure = {
            "InterestCategory": {
                "fields": {
                    "id": "integer",
                    "name": "string"
                }
            },
            "CustomUser": {
                "fields": {
                    "id": "integer",
                    "username": "string",
                    "email": "string",
                    "phoneNum": "string",
                    "birth": "date",
                    "full_name": "string",
                    "school": "string (nullable)",
                    "department": "string (nullable)",
                    "admission_date": "date (nullable)",
                    "graduation_date": "date (nullable)",
                    "experience": "json (nullable)",
                    "self_introduction": "string (nullable)",
                    "companies_of_interest": "string (nullable)",
                    "reservation_status": "json (nullable)",
                    "interest_categories": "list of InterestCategory IDs (many-to-many relationship)"
                }
            },
            "Company": {
                "fields": {
                    "id": "integer",
                    "name": "string",
                    "company_id": "string",
                    "promotional_content": "string",
                    "applicants": "list of CustomUser IDs (many-to-many relationship)",
                    "manager": "string",
                    "password": "string (hashed)",
                    "completed_consultations": "list of CustomUser IDs (many-to-many relationship)"
                }
            },
            "Booth": {
                "fields": {
                    "booth_id": "integer (primary key)",
                    "company": "Company ID (foreign key)",
                    "day": "string",
                    "floor": "string",
                    "boothNum": "string (nullable)",
                    "boothCate": "string (nullable)",
                    "boothName": "string (nullable)",
                    "queue": "list of CustomUser IDs (many-to-many relationship)",
                    "current_consultation": "integer (nullable)",
                    "wait_time": "integer (default: 0)"
                }
            },
            "BoothQueue": {
                "fields": {
                    "id": "integer",
                    "booth": "Booth ID (foreign key)",
                    "user": "CustomUser ID (foreign key)",
                    "position": "integer"
                }
            }
        }
        return JsonResponse(data_structure)
