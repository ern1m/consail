from rest_framework import serializers

from consailapi.consultations.consts import ReservationDurationInt
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


class UUIDListSerializer(serializers.Serializer):
    uuids = serializers.ListField(
        child=serializers.UUIDField(), allow_empty=True, required=True
    )


class ReservationTimeSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()


class ReservationTimeAndUuidsSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    uuids = serializers.ListField(child=serializers.UUIDField())


class ReservationDurationSerializer(serializers.Serializer):
    duration = serializers.ChoiceField(choices=ReservationDurationInt.choices)
