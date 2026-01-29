import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Dataset
from .serializers import DatasetSerializer


class UploadCSV(APIView):

    def post(self, request):

        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # Read CSV
        df = pd.read_csv(file)

        # Calculate summary
        summary = {
            "total": len(df),
            "avg_flow": float(df["Flowrate"].mean()),
            "avg_pressure": float(df["Pressure"].mean()),
            "avg_temp": float(df["Temperature"].mean()),
            "type_dist": df["Type"].value_counts().to_dict()
        }

        # Save in DB
        Dataset.objects.create(
            name=file.name,
            file=file,
            summary=summary
        )

        # Keep only last 5 uploads
        all_data = Dataset.objects.order_by('-uploaded_at')

        if all_data.count() > 5:
            for d in all_data[5:]:
                d.delete()

        return Response(summary)


class History(APIView):

    def get(self, request):

        data = Dataset.objects.order_by('-uploaded_at')[:5]

        serializer = DatasetSerializer(data, many=True)

        return Response(serializer.data)
