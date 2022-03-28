from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"


class FundWalletSerializer(serializers.ModelSerializer):
    balance = serializers.IntegerField()

    class Meta:
        model = Wallet
        fields = [
            "balance"
        ]

    def update(self, instance, validated_data):
        instance.wallet.balance = validated_data.get("balance", instance.wallet.balance)

        return super().update(instance, validated_data)