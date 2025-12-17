from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    FarmerProfileCreateSerializer,
    FarmerProfileDetailsSerializer,
    FarmerProfilesListSerializer,
    ProductDetailsSerializer,
    ProductListSerializer,
    ProductCreateSerializer
)
from ..models import FarmerProfile,ProductListing
from shared.responses import (
    handle_success,
    handle_error,
    handle_validation_error,
    handle_not_found,
)


class FarmerProfileCreateView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=['Profiles (Farmer)'],
        request_body=FarmerProfileCreateSerializer,
        responses={
            201: FarmerProfileDetailsSerializer,
            400: 'Bad Request',
            500: 'Internal Server Error'
        },
        description="Create a farmer profile for the authenticated user."
    )
    def post(self, request):
        user=request.user
        if hasattr(user, 'farmer_profile'):
            return handle_error(
                message="Farmer profile already exists.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer = FarmerProfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                farmer_profile = serializer.save(user=user)
                profile_serializer = FarmerProfileDetailsSerializer(farmer_profile)
                return handle_success(
                    data=profile_serializer.data,
                    message="Farmer profile created successfully.",
                    status_code=status.HTTP_201_CREATED
                )
            except Exception:
                return handle_error(
                    message="An error occurred while creating the farmer profile.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return handle_validation_error(
            errors=serializer.errors,
            message="Validation failed.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class FarmerProfileUpdateView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profiles (Farmer)'],
        request_body=FarmerProfileCreateSerializer,
        responses={
            200: FarmerProfileDetailsSerializer,
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        description="Update the farmer profile of the authenticated user."
    )
    def patch(self, request):
        user = request.user
        try:
            farmer_profile = user.farmer_profile
        except FarmerProfile.DoesNotExist:
            return handle_not_found(
                message="Farmer profile not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = FarmerProfileCreateSerializer(farmer_profile, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_profile = serializer.save()
                profile_serializer = FarmerProfileDetailsSerializer(updated_profile)
                return handle_success(
                    data=profile_serializer.data,
                    message="Farmer profile updated successfully.",
                    status_code=status.HTTP_200_OK
                )
            except Exception:
                return handle_error(
                    message="An error occurred while updating the farmer profile.",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return handle_validation_error(
            errors=serializer.errors,
            message="Validation failed.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class FarmerProfileDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profiles (Farmer)'],
        responses={
            200: FarmerProfileDetailsSerializer,
            404: 'Not Found',
            500: 'Internal Server Error'

        },
        description="Retrieve the farmer profile of the authenticated user."
    )
    def get(self, request):
        user = request.user
        try:
            farmer_profile = user.farmer_profile
            serializer = FarmerProfileDetailsSerializer(farmer_profile)
            return  handle_success(
                data=serializer.data,
                message="Farmer profile retrieved successfully.",
                status_code=status.HTTP_200_OK
            )
        except FarmerProfile.DoesNotExist:
            return handle_not_found(
                message="Farmer profile not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

# get farmer profile by ID
class FarmerProfileByIDView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profiles (Farmer)'],
        responses={
            200: FarmerProfileDetailsSerializer,
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        description="Retrieve a farmer profile by its ID."
    )
    def get(self, request, profile_id):
        try:
            farmer_profile = FarmerProfile.objects.get(id=profile_id)
            serializer = FarmerProfileDetailsSerializer(farmer_profile)
            return handle_success(
                data=serializer.data,
                message="Farmer profile retrieved successfully.",
                status_code=status.HTTP_200_OK
            )
        except FarmerProfile.DoesNotExist:
            return handle_not_found(
                message="Farmer profile not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return handle_error(
                message="An error occurred while retrieving the farmer profile.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class FarmerProfilesListView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profiles (Farmer)'],
        responses={
            200: FarmerProfilesListSerializer(many=True),
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        description="Retrieve a list of all farmer profiles."
    )
    def get(self, request):
        try:
            farmer_profiles = FarmerProfile.objects.all()
            serializer = FarmerProfilesListSerializer(farmer_profiles, many=True)
            return handle_success(
                data=serializer.data,
                message="Farmer profiles retrieved successfully.",
                status_code=status.HTTP_200_OK
            )
        except Exception:
            return handle_error(
                message="An error occurred while retrieving farmer profiles.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteFarmerProfileView(APIView):
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Profiles (Farmer)'],
        responses={
            200: 'Farmer profile deleted successfully.',
            404: 'Not Found',
            500: 'Internal Server Error'
        },
        description="Delete the farmer profile of the authenticated user."
    )
    def delete(self, request):
        user = request.user
        try:
            farmer_profile = user.farmer_profile
            farmer_profile.delete()
            return handle_success(
                message="Farmer profile deleted successfully.",
                status_code=status.HTTP_200_OK
            )
        except FarmerProfile.DoesNotExist:
            return handle_not_found(
                message="Farmer profile not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return handle_error(
                message="An error occurred while deleting the farmer profile.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )