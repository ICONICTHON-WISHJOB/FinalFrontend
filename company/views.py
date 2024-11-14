from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Booth, Company, CustomUser

class WaitCountView(APIView):
    @swagger_auto_schema(
        operation_summary="Get wait count for a specific booth by company ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the company associated with the booth",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Wait count response",
                examples={
                    "application/json": {
                        "waitCnt": 4
                    }
                }
            ),
            404: "Booth or Company not found"
        }
    )
    def get(self, request, id):
        # Fetch the company with the given id
        try:
            company = Company.objects.get(id=id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the booth associated with the company
        booth = Booth.objects.filter(company=company).first()
        if not booth:
            return Response({"error": "Booth not found for the given company"}, status=status.HTTP_404_NOT_FOUND)

        # Count the queue for the booth
        wait_count = booth.queue.count()
        return Response({"waitCnt": wait_count}, status=status.HTTP_200_OK)


class WaitListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get wait list for a specific booth by company ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the company associated with the booth",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Wait list response",
                examples={
                    "application/json": {
                        "users": [
                            {
                                "user_id": "test@example.com",
                                "full_name": "김도현",
                            },
                            {
                                "user_id": "test2@example.com",
                                "full_name": "박지수",
                            }
                        ],
                        "totalCnt": 2
                    }
                }
            ),
            404: "Booth or Company not found"
        }
    )
    def get(self, request, id):
        # Fetch the company with the given id
        try:
            company = Company.objects.get(id=id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the booth associated with the company
        booth = Booth.objects.filter(company=company).first()
        if not booth:
            return Response({"error": "Booth not found for the given company"}, status=status.HTTP_404_NOT_FOUND)

        # Get all users in the booth queue
        users_in_queue = booth.queue.all()
        user_data = [
            {
                "user_id": user.email,
                "full_name": user.full_name
            }
            for user in users_in_queue
        ]

        # Prepare the response
        response_data = {
            "users": user_data,
            "totalCnt": users_in_queue.count()
        }

        return Response(response_data, status=status.HTTP_200_OK)