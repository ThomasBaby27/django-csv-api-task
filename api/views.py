import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from .serializers import UserSerializer
from .models import User

class UserUploadView(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            return Response({"error": "Only .csv files are allowed."}, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        success_count = 0
        errors = []
        for row in reader:
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                try:
                    serializer.save()
                    success_count += 1
                except Exception:
                    errors.append({"row": row, "error": "Email already exists."})
            else:
                errors.append({"row": row, "errors": serializer.errors})
        return Response({
            "total_saved": success_count,
            "total_rejected": len(errors),
            "validation_errors": errors
        }, status=status.HTTP_201_CREATED)

