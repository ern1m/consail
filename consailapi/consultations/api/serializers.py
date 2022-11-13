from rest_framework import serializers

from consailapi.consultations.models import Consultation


class ConsultationSimpleActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ["start_time", "end_time"]
