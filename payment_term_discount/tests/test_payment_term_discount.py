from dateutil.relativedelta import relativedelta

from odoo import fields, Command
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install')
class TestPaymentTermDiscount(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner1 = cls.env['res.partner'].create({'name': 'Partner1'})

        cls.product_template1 = cls.env['product.template'].create({
            'name': 'Test Product1',
            'list_price': 100.0,
            'standard_price': 80.0,
            'type': 'consu',
        })

        cls.product1 = cls.product_template1.product_variant_id

        cls.payment_term1 = cls.env['account.payment.term'].create({
            'name': 'Payment Term1',
        })

        cls.payment_term2 = cls.env['account.payment.term'].create({
            'name': 'Payment Term2',
            'early_discount': True,
            'early_payment_discount_ids': [
                Command.create({
                'payment_term_id': cls.id,
                'discount_percentage': 2.0,
                'discount_days': 10,
                }),
                Command.create({
                    'payment_term_id': cls.id,
                    'discount_percentage': 1.0,
                    'discount_days': 5,
                }),
            ],
        })

        cls.invoice1 = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner1.id,
            'invoice_payment_term_id': cls.payment_term1.id,
            'invoice_line_ids': [
                Command.create({'product_id': cls.product1.id}),
            ],
        })

        cls.invoice2 = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner1.id,
            'invoice_payment_term_id': cls.payment_term2.id,
            'invoice_line_ids': [
                Command.create({'product_id': cls.product1.id}),
            ],
        })

    def test_early_payment_discount(cls):
        cls.invoice1.action_post()
        cls.invoice1.action_register_payment()

        payment_wizard1 = cls.env['account.payment.register'].with_context({
            'active_model': 'account.move',
            'active_ids': [cls.invoice1.id],
        }).create({'payment_date': fields.Date.today()})

        payment_wizard1._create_payments()
        cls.assertEqual(payment_wizard1.payment_difference, 0.0, "Payment difference should be zero becuase the early discount is turned off for the selected payment term")

        cls.invoice2.action_post()
        cls.invoice2.action_register_payment()

        payment_wizard2 = cls.env['account.payment.register'].with_context({
            'active_model': 'account.move',
            'active_ids': [cls.invoice2.id],
        }).create({'payment_date': fields.Date.today()})
        cls.assertEqual(payment_wizard2.payment_difference, 2.3, "Early payment discount does not applied properly for selected payment date")

        payment_wizard2.payment_date = fields.Date.today() + relativedelta(days=(15))
        cls.assertEqual(payment_wizard2.payment_difference, 1.15, "Early payment discount does not applied properly after changing the payment date")

        payment_wizard2.payment_date = fields.Date.today() + relativedelta(days=(16))
        cls.assertEqual(payment_wizard2.payment_difference, 0.0, "Early payment discount should be zero after expiry of the early payment discounts")
