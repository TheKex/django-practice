from rest_framework import serializers
from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description"]


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ["product", "quantity", "price"]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, required=False)

    class Meta:
        model = Stock
        fields = ["id", "address", "positions"]

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = []
        if 'positions' in validated_data:
            positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            obj, created = StockProduct.objects.create(stock=stock, **position)
            obj.save()
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = []
        if 'positions' in validated_data:
            positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            obj, created = StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults=position
            )
            obj.save()

        return stock
