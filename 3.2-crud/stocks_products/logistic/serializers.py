from rest_framework import serializers

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    # настройте сериализатор для склада

    def create(self, validated_data):
        # print(validated_data)
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # создаем склад по его параметрам
        # print('----\n', positions)
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            values = {
                'product': position['product'],
                'quantity': position['quantity'],
                'price': position['price'],
                'stock': stock
            }
            StockProduct.objects.create(**values)

        return stock

    def update(self, instance, validated_data):
        print(validated_data)
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        print(stock)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            values = {
                'product': position['product'],
                'quantity': position['quantity'],
                'price': position['price'],
                'stock': stock
            }
            StockProduct.objects.update_or_create(**values)

        return stock
