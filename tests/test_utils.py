import unittest
import ces.utils as utils
from ces.models import Wallet, Currency
from ces.exceptions import InvalidAmountException

class TestUtils(unittest.TestCase):
    def test_rounding_by_whole_numbers(self):
        self.assertEqual(1.0, utils.round_order_value(1.0, 1.0))
        self.assertEqual(2.0, utils.round_order_value(1.0, 2.0))
        self.assertEqual(2.0, utils.round_order_value(1.0, 2.5))
        self.assertEqual(0.0, utils.round_order_value(1.0, 0.5))
        self.assertEqual(10.0, utils.round_order_value(10.0, 16.0))
        self.assertEqual(100.0, utils.round_order_value(100.0, 115.0))

    def test_rounding_by_decimals(self):
        self.assertEqual(0.05, utils.round_order_value(0.001, 0.05056087))
        self.assertEqual(0.051, utils.round_order_value(0.001, 0.051))
        self.assertEqual(0.2, utils.round_order_value(0.001, 0.2001))
        self.assertEqual(0.1, utils.round_order_value(0.1, 0.11))
        self.assertEqual(0.5, utils.round_order_value(0.1, 0.56))
        self.assertEqual(1.5, utils.round_order_value(0.1, 1.56))
        self.assertEqual(1.56, utils.round_order_value(0.01, 1.56666))

    def test_appropriate_float_format_string(self):
        self.assertEqual(
            '100.000',
            utils.make_appropriate_float_format_string(100.0).format(100.0)
        )
        self.assertEqual(
            '10.0000',
            utils.make_appropriate_float_format_string(10.0).format(10.0)
        )
        self.assertEqual(
            '1.00000',
            utils.make_appropriate_float_format_string(1.0).format(1.0)
        )
        self.assertEqual(
            '0.01000',
            utils.make_appropriate_float_format_string(0.01).format(0.01)
        )
        self.assertEqual(
            '0.00100',
            utils.make_appropriate_float_format_string(0.001).format(0.001)
        )
        self.assertEqual(
            '0.000100',
            utils.make_appropriate_float_format_string(0.00010).format(0.00010)
        )
        self.assertEqual(
            '0.0000100',
            utils.make_appropriate_float_format_string(0.00001).format(0.00001)
        )
        self.assertEqual(
            '0.00000100',
            utils.make_appropriate_float_format_string(0.000001).format(0.000001)
        )

    def test_coin_price(self):
        self.assertEqual(
            '15 XLM',
            utils.CoinPrice('XLM').format_value(15)
        )
        self.assertEqual(
            '15 XLM ($30)',
            utils.CoinPrice('XLM', 2, 'usd').format_value(15)
        )
        self.assertEqual(
            '15 XLM (AU$ 45)',
            utils.CoinPrice('XLM', 3, 'aud').format_value(15)
        )

    def test_operation_amount(self):
        wallet = Wallet(
            Currency('XLM', 'Lumens', None, None), 
            200,
            200,
            0
        )
        # Sell tests
        self.assertEqual(
            200,
            utils.OrderAmount('max').compute_sell_units(wallet)
        )
        self.assertEqual(
            50,
            utils.OrderAmount('25%').compute_sell_units(wallet)
        )
        self.assertEqual(
            117,
            utils.OrderAmount('117').compute_sell_units(wallet)
        )
        self.assertEqual(
            0.1,
            utils.OrderAmount('0.1').compute_sell_units(wallet)
        )
        # Buy tests
        self.assertEqual(
            100,
            utils.OrderAmount('max').compute_purchasable_units(wallet, 2.0)
        )
        self.assertEqual(
            400,
            utils.OrderAmount('max').compute_purchasable_units(wallet, 0.5)
        )
        self.assertEqual(
            25,
            utils.OrderAmount('25%').compute_purchasable_units(wallet, 2.0)
        )
        self.assertEqual(
            150,
            utils.OrderAmount('150').compute_purchasable_units(wallet, 2.0)
        )
        self.assertEqual(
            0.1,
            utils.OrderAmount('0.1').compute_purchasable_units(wallet, 2.0)
        )
        # Failure cases
        self.assertRaises(
            InvalidAmountException,
            lambda: utils.OrderAmount('101%').compute_sell_units(wallet)
        )
        self.assertRaises(
            InvalidAmountException,
            lambda: utils.OrderAmount('0%').compute_sell_units(wallet)
        )
        self.assertRaises(
            InvalidAmountException,
            lambda: utils.OrderAmount('-1%').compute_sell_units(wallet)
        )
        self.assertRaises(
            InvalidAmountException,
            lambda: utils.OrderAmount('a%').compute_sell_units(wallet)
        )
        self.assertRaises(
            InvalidAmountException,
            lambda: utils.OrderAmount('10 1').compute_sell_units(wallet)
        )
        self.assertRaises(
            InvalidAmountException,
            lambda: utils.OrderAmount('-1').compute_sell_units(wallet)
        )
