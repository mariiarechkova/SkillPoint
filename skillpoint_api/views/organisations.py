from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import OrganisationSerializer, UserSerializer
from ..models import Organisation, User


class OrganisationsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        organisations = Organisation.objects.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        organisation_data = {
            'name': request.data.get('organisation_name')
        }
        user_email = request.data.get('email')
        user_exist = User.objects.filter(email=user_email).exists()
        if user_exist:
            return Response({"message": "User with this email already exists."}, status=400)
        else:
            org_serializer = OrganisationSerializer(data=organisation_data)
            if org_serializer.is_valid():
                created_organisation = org_serializer.save()

                user_data = request.data.copy()
                user_data['organisation'] = created_organisation.id
                user_data['is_staff'] = True
                user_serializer = UserSerializer(data=user_data)

                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({
                        'organisation': org_serializer.data,
                        'user': user_serializer.data
                     }, status=status.HTTP_201_CREATED)
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(org_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
