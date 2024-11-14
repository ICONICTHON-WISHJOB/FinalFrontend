from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser, Company, Booth, BoothQueue
from users.serializers import BoothSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

class ReserveBoothView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booth_id):
        user = request.user
        try:
            booth = Booth.objects.get(id=booth_id)
        except Booth.DoesNotExist:
            return Response({"error": "Booth not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already in the queue
        if BoothQueue.objects.filter(booth=booth, user=user).exists():
            return Response({"message": "Already in the queue"}, status=status.HTTP_400_BAD_REQUEST)

        # Add user to the queue
        position = BoothQueue.objects.filter(booth=booth).count() + 1
        BoothQueue.objects.create(booth=booth, user=user, position=position)

        return Response({"message": f"Added to queue at position {position}"}, status=status.HTTP_201_CREATED)

class CheckQueuePositionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, booth_id):
        user = request.user
        try:
            queue_entry = BoothQueue.objects.get(booth_id=booth_id, user=user)
            position = queue_entry.position
            return Response({"position": position}, status=status.HTTP_200_OK)
        except BoothQueue.DoesNotExist:
            return Response({"error": "You are not in the queue for this booth"}, status=status.HTTP_404_NOT_FOUND)


class BoothListView(APIView):
    def get(self, request, day, floor):
        booths = Booth.objects.filter(day=day, floor=floor)
        serializer = BoothSerializer(booths, many=True)
        return Response({"booths": serializer.data}, status=status.HTTP_200_OK)


class BoothApplyView(APIView):
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                          description='ID of the user making the reservation'),
                'booth_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the booth'),
            },
            required=['user_id', 'booth_id'],
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'boothName': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the booth'),
                'waitTime': openapi.Schema(type=openapi.TYPE_INTEGER, description='Calculated wait time in minutes'),
            }
        )}
    )

    def post(self, request):
        user_id = request.data.get('user_id')  # unique ID for the user
        booth_id = request.data.get('booth_id')

        # Fetch the user by ID
        user = get_object_or_404(CustomUser, id=user_id)
        # Fetch the booth by ID
        booth = get_object_or_404(Booth, booth_id=booth_id)

        booth.queue.add(user)
        booth.wait_time = booth.calculate_wait_time()

        return Response({
            "boothName": booth.boothName,
            "waitTime": booth.wait_time
        }, status=status.HTTP_200_OK)