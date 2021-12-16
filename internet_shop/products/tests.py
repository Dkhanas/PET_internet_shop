from django.test import TransactionTestCase
from .models import Category, Currency, Product, Characteristic
from django.db.utils import DataError, IntegrityError
from django.core.exceptions import ValidationError


class CatalogTestCase(TransactionTestCase):
    parent_id_text = '13d2bb27-6f71-4938-8fdc-a12ffbe67992'
    computer_id_upd = '63da31b5-0ba9-48e5-9e13-83995f8435d6'
    computer_laptops_text = "Computer and Laptops"
    laptop_text = "Laptop"
    computer_text = "Computer"

    def setUp(self):
        computer_laptops = Category.objects.create(id=self.parent_id_text, name=self.computer_laptops_text)
        Category.objects.create(name=self.computer_text, parent=computer_laptops)

    def test_success_create_get_delete_methods(self):
        computer_laptops = Category.objects.get(name=self.computer_laptops_text)
        laptops = Category.objects.create(name=self.laptop_text, parent=computer_laptops)
        self.assertEqual(computer_laptops.name, self.computer_laptops_text)
        self.assertEqual(str(computer_laptops.id), self.parent_id_text)
        self.assertTrue(laptops)
        self.assertEqual(str(laptops), laptops.name)
        self.assertEqual(laptops.name, self.laptop_text)
        self.assertEqual(laptops.parent, computer_laptops)
        self.assertEqual((3, {'products.Catalog': 3}), computer_laptops.delete())

    def test_success_update_method(self):
        update_laptop_text = "Not Laptops"
        equipment_text = "Equipment"
        computer_laptops = Category.objects.get(name=self.computer_laptops_text)
        equipment = Category.objects.create(name=equipment_text)
        computer_laptops.name = update_laptop_text
        computer_laptops.id = self.computer_id_upd
        computer_laptops.parent = equipment
        computer_laptops.save()
        self.assertEqual(computer_laptops.name, update_laptop_text)
        self.assertEqual(computer_laptops.id, self.computer_id_upd)
        self.assertEqual(computer_laptops.parent, equipment)

    def test_fail_methods(self):
        huge_text = "a" * 300
        self.assertRaises(ValueError, Category.objects.create, name=self.laptop_text, parent="fail")
        self.assertRaises(DataError, Category.objects.create, id=20, name=self.id)
        self.assertRaises(DataError, Category.objects.create, name=huge_text)
        self.assertRaises(ValidationError, Category.objects.get, parent="fwafwa")
        self.assertRaises(IntegrityError, Category.objects.create, id=self.parent_id_text, name=self.computer_laptops_text)
        computer_laptops = Category.objects.get(name=self.computer_laptops_text)
        computer_laptops.name = huge_text
        self.assertRaises(DataError, computer_laptops.save)
        computer_laptops.delete()
        try:
            computer_laptops = Category.objects.get(name=self.computer_laptops_text)
        except Category.DoesNotExist:
            computer_laptops = 'Catalog.DoesNotExist'
        self.assertEqual('Catalog.DoesNotExist', computer_laptops)


class CurrencyTestCase(TransactionTestCase):
    currency_id = '13d2bb27-6f71-4938-8fdc-a12ffbe67992'
    currency_id_upd = '63da31b5-0ba9-48e5-9e13-83995f8435d6'
    currency_text = "USD"
    uah_text = "UAH"
    exchange_rate = 1
    uah_exchange_rate = 26.55
    def setUp(self):
        Currency.objects.create(id=self.currency_id, name=self.currency_text, exchange_rate=self.exchange_rate)

    def test_success_create_get_delete_methods(self):
        currency_usd_get_by_name = Currency.objects.get(name=self.currency_text)
        currency_usd_get_by_id = Currency.objects.get(id=self.currency_id)
        currency_usd_get_by_exchange_rate = Currency.objects.get(exchange_rate=self.exchange_rate)
        self.assertEqual(currency_usd_get_by_name.name, self.currency_text)
        self.assertEqual(currency_usd_get_by_exchange_rate.exchange_rate, self.exchange_rate)
        self.assertEqual(str(currency_usd_get_by_id.id), self.currency_id)
        currency_uah = Currency.objects.create(name=self.uah_text, exchange_rate=self.uah_exchange_rate)
        self.assertTrue(currency_uah)
        self.assertEqual(str(currency_uah), self.uah_text)
        self.assertEqual((1, {'products.Currency': 1}), currency_uah.delete())

    def test_success_update_method(self):
        currency_usd = Currency.objects.get(id=self.currency_id)
        currency_usd.name = self.uah_text
        currency_usd.id = self.currency_id_upd
        currency_usd.exchange_rate = self.uah_exchange_rate
        currency_usd.save()
        self.assertEqual(currency_usd.name, self.uah_text)
        self.assertEqual(currency_usd.id, self.currency_id_upd)
        self.assertEqual(currency_usd.exchange_rate, self.uah_exchange_rate)

    def test_fail_methods(self):
        huge_text = "a" * 300
        fail_text = "fail"
        self.assertRaises(ValidationError, Currency.objects.create, name=self.uah_text, exchange_rate=fail_text)
        self.assertRaises(IntegrityError, Currency.objects.create, id=self.currency_id_upd, name=self.uah_text)
        self.assertRaises(ValidationError, Currency.objects.create, id='adw', name=self.uah_text, exchange_rate=self.exchange_rate)
        self.assertRaises(ValidationError, Currency.objects.create, id=self.currency_id_upd, name=self.uah_text, exchange_rate=fail_text)
        self.assertRaises(DataError, Currency.objects.create, name=huge_text)
        self.assertRaises(DataError, Currency.objects.create, name=self.currency_text, exchange_rate=23243252525252.34)
        self.assertRaises(ValidationError, Currency.objects.get, exchange_rate=fail_text)
        currency = Currency.objects.get(id=self.currency_id)
        currency.name = huge_text
        self.assertRaises(DataError, currency.save)
        currency.name = self.exchange_rate
        currency.exchange_rate = fail_text
        self.assertRaises(ValidationError, currency.save)
        currency.exchange_rate = 4165165816.4115715
        self.assertRaises(DataError, currency.save)
        currency.delete()
        try:
            currency = Category.objects.get(name=self.currency_text)
        except Category.DoesNotExist:
            currency = 'Currency.DoesNotExist'
        self.assertEqual('Currency.DoesNotExist', currency)


class ProductTestCase(TransactionTestCase):
    product_id = '13d2bb27-6f71-4938-8fdc-a12ffbe67992'
    product_id_upd = '63da31b5-0ba9-48e5-9e13-83995f8435d6'
    product_name_text = "Apple"
    product_name_upd = "Orange"
    product_description_text = "It's a fruit"
    product_price = 23.14
    product_image = 'https://www.pinterest.ru/pin/358388082854841306/'
    product_quantity = 1
    product_quantity_upd = 2

    def setUp(self):
        Product.objects.create(id=self.product_id,
                               name=self.product_name_text,
                               description=self.product_description_text,
                               price=self.product_price,
                               image=self.product_image,
                               quantity=self.product_quantity)

    def test_success_create_get_delete_methods(self):
        product_by_name = Product.objects.get(name=self.product_name_text)
        product_by_id = Product.objects.get(id=self.product_id)
        self.assertEqual(product_by_name.name, self.product_name_text)
        self.assertEqual(str(product_by_id.id), self.product_id)
        self.assertTrue(product_by_id)
        self.assertEqual(str(product_by_id), self.product_name_text)
        self.assertEqual((1, {'products.Product': 1}), product_by_name.delete())

    def test_success_update_method(self):
        product_by_id = Product.objects.get(id=self.product_id)
        product_by_id.id = self.product_id_upd
        product_by_id.name = self.product_name_upd
        product_by_id.quantity = self.product_quantity_upd
        product_by_id.save()
        self.assertEqual(product_by_id.name, self.product_name_upd)
        self.assertEqual(product_by_id.id, self.product_id_upd)
        self.assertEqual(product_by_id.quantity, self.product_quantity_upd)

    # TODO: add tests
    def test_fail_methods(self):
        pass


# TODO: add tests
class CharacteristicTestCase(TransactionTestCase):
    pass
