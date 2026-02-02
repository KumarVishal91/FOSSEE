import io

import pandas as pd
from django.http import FileResponse, Http404
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Dataset
from .serializers import DatasetDetailSerializer, DatasetListSerializer


REQUIRED_COLUMNS = [
    "Equipment Name",
    "Type",
    "Flowrate",
    "Pressure",
    "Temperature",
]


def _build_summary(df: pd.DataFrame) -> dict:
    return {
        "total": int(len(df)),
        "avg_flow": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temp": float(df["Temperature"].mean()),
        "type_dist": df["Type"].value_counts().to_dict(),
    }


class UploadCSV(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        # Read CSV
        try:
            df = pd.read_csv(file)
        except Exception:
            return Response({"error": "Invalid CSV file"}, status=400)

        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            return Response(
                {"error": "Missing required columns", "missing": missing},
                status=400,
            )

        df = df[REQUIRED_COLUMNS].copy()
        df["Flowrate"] = pd.to_numeric(df["Flowrate"], errors="coerce")
        df["Pressure"] = pd.to_numeric(df["Pressure"], errors="coerce")
        df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
        df = df.dropna(subset=["Flowrate", "Pressure", "Temperature", "Type"])

        summary = _build_summary(df)

        file.seek(0)
        dataset = Dataset.objects.create(
            name=file.name,
            file=file,
            summary=summary,
            row_count=int(len(df)),
            columns=REQUIRED_COLUMNS,
            data=df.to_dict(orient="records"),
        )

        # Keep only last 5 uploads
        all_data = Dataset.objects.order_by("-uploaded_at")
        if all_data.count() > 5:
            for old in all_data[5:]:
                old.delete()

        return Response(DatasetDetailSerializer(dataset).data)


class History(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = Dataset.objects.order_by("-uploaded_at")[:5]
        serializer = DatasetListSerializer(data, many=True)
        return Response(serializer.data)


class DatasetDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

        return Response(DatasetDetailSerializer(dataset).data)


class LatestDataset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dataset = Dataset.objects.order_by("-uploaded_at").first()
        if not dataset:
            return Response({"detail": "No datasets"}, status=404)
        return Response(DatasetDetailSerializer(dataset).data)


class DatasetReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        pdf.setTitle(f"Dataset Report - {dataset.name}")
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(1 * inch, 10.5 * inch, "Chemical Equipment Report")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(1 * inch, 10.0 * inch, f"Dataset: {dataset.name}")
        pdf.drawString(1 * inch, 9.7 * inch, f"Uploaded: {dataset.uploaded_at}")
        pdf.drawString(1 * inch, 9.4 * inch, f"Total Records: {dataset.row_count}")

        summary = dataset.summary or {}
        pdf.drawString(1 * inch, 8.9 * inch, f"Average Flowrate: {summary.get('avg_flow', 0):.2f}")
        pdf.drawString(1 * inch, 8.6 * inch, f"Average Pressure: {summary.get('avg_pressure', 0):.2f}")
        pdf.drawString(1 * inch, 8.3 * inch, f"Average Temperature: {summary.get('avg_temp', 0):.2f}")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(1 * inch, 7.8 * inch, "Type Distribution")
        pdf.setFont("Helvetica", 11)

        y = 7.5 * inch
        for equipment_type, count in (summary.get("type_dist") or {}).items():
            pdf.drawString(1 * inch, y, f"{equipment_type}: {count}")
            y -= 0.25 * inch
            if y < 1.25 * inch:
                pdf.showPage()
                y = 10.5 * inch

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f"dataset-report-{dataset.pk}.pdf",
            content_type="application/pdf",
        )
