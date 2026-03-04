from rest_framework import serializers

class WESADFeaturesSerializer(serializers.Serializer):
    """Validates the 27 nested features from the WESAD dataset"""
    hr_mean = serializers.FloatField()
    hr_std = serializers.FloatField()
    hr_min = serializers.FloatField()
    hr_max = serializers.FloatField()
    hr_range = serializers.FloatField()
    
    eda_mean = serializers.FloatField()
    eda_std = serializers.FloatField()
    eda_min = serializers.FloatField()
    eda_max = serializers.FloatField()
    eda_range = serializers.FloatField()
    
    bvp_mean = serializers.FloatField()
    bvp_std = serializers.FloatField()
    bvp_min = serializers.FloatField()
    bvp_max = serializers.FloatField()
    bvp_range = serializers.FloatField()
    
    ibi_mean = serializers.FloatField()
    ibi_std = serializers.FloatField()
    ibi_min = serializers.FloatField()
    ibi_max = serializers.FloatField()
    ibi_range = serializers.FloatField()
    ibi_rmssd = serializers.FloatField()
    
    acc_mag_mean = serializers.FloatField()
    acc_mag_std = serializers.FloatField()
    acc_mag_min = serializers.FloatField()
    acc_mag_max = serializers.FloatField()
    acc_mag_range = serializers.FloatField()
    acc_activity = serializers.FloatField()


class RiskResultSerializer(serializers.Serializer):
    """Validates the incoming JSON payload before saving to MongoDB"""
    user_id = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()
    features = WESADFeaturesSerializer() 
    risk_level = serializers.CharField(max_length=20)
    
    # --- ADD THESE FOR AMER'S AI OUTPUT ---
    confidence = serializers.FloatField(required=False)
    summary = serializers.CharField(required=False, allow_blank=True)
    recommendation = serializers.CharField(required=False, allow_blank=True)