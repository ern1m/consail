from rest_framework import serializers

from consailapi.consultations.models import Consultation, Reservation
from consailapi.students.api.serializers import StudentDetailSerializer


class ConsultationSimpleActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ["uuid", "start_time", "end_time"]


class ReservationSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer()

    class Meta:
        model = Reservation
        fields = ["uuid", "student", "is_cancelled", "start_time", "end_time"]


class ConsultationDetailSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True)

    class Meta:
        model = Consultation
        fields = ["uuid", "start_time", "end_time", "reservations"]


class ReservationUuidSerializer(serializers.ModelSerializer):
    reservation_uuid = serializers.UUIDField()

    class Meta:
        model = Reservation
        fields = [
            "reservation_uuid",
        ]
