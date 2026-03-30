from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Vendor
from .serializers import VendorSerializer

class CreateVendorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != 'vendor':
            raise PermissionDenied("Only users with vendor role allowed")

        if hasattr(user, 'vendor'):
            return Response({"error": "Vendor profile already exists"})

        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)

        return Response(serializer.errors)

class VendorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'vendor'):
            return Response({"error": "Vendor not found"})

        vendor = request.user.vendor
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

class UpdateVendorView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        vendor = request.user.vendor

        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
