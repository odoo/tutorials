from dateutil.relativedelta import relativedelta
from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestBetterRibbons(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.website = cls.env['website'].search([], limit=1)
        cls.product = cls.env['product.template'].search([], limit=1)
        cls.product.write({
            'has_manual_ribbon': False,
            'website_ribbon_id': False,
            'is_published': True,
            'publish_date': fields.Date.today() - relativedelta(days=5),
        })

        cls.sale_pricelist = cls.env['product.pricelist'].search(
            [('name', '=', 'Christmas')], limit=1
        )
        cls.sale_pricelist.write({'selectable': True})
        cls.website.write({'pricelist_id': cls.sale_pricelist.id})

        cls.prices = cls.product._get_sales_prices(cls.website).get(cls.product.id)

    def _create_ribbon(self, name, assign='manually', style='ribbon'):
        return self.env['product.ribbon'].create({
            'name': name,
            'assign': assign,
            'style': style,
            'sequence': 1,
        })

    def test_1_new_ribbon(self):
        ribbon = self._create_ribbon('New', 'new')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            'New ribbon should be assigned to the product when publish date is today.',
        )

    def test_2_sale_ribbon(self):
        self._create_ribbon('New', 'new')

        ribbon = self._create_ribbon('Sale', 'sale')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            'Sale ribbon should be assigned to the product when discount is applied.',
        )

    def test_3_out_of_stock_ribbon(self):
        self.product.write({'qty_available': 0, 'allow_out_of_stock_order': False})
        self._create_ribbon('Sale', 'sale')
        self._create_ribbon('New', 'new')

        oos_ribbon = self._create_ribbon('Out of Stock', 'out_of_stock')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            oos_ribbon.id,
            'Out of Stock ribbon should take priority over Sale ribbon.',
        )

    def test_4_manual_ribbon(self):
        manual = self._create_ribbon('Manual', 'manually')
        self.product.write({
            'website_ribbon_id': manual.id,
            'publish_date': fields.Date.today(),
        })
        self._create_ribbon('New', 'new')
        self.product._set_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            manual.id,
            'Automatic ribbons should not override manually assigned ribbons.',
        )

    def test_5_allow_out_of_stock_flag(self):
        ribbon = self._create_ribbon('Out of Stock', 'out_of_stock')

        self.product.write({'qty_available': 0, 'allow_out_of_stock_order': True})
        self.product._set_ribbon(self.prices)
        self.assertNotEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            'When allow_out_of_stock_order is True,'
            'the Out of Stock ribbon should not be assigned.',
        )
