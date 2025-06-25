from odoo.tests.common import TransactionCase
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestBookPrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestBookPrice,cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.product = cls.env['product.product'].create({
            'name':'Test Product',
            'list_price': 100,
            'type' :'consu',
            'invoice_policy': 'order',
        })
        cls.pricelist = cls.env["product.pricelist"].create({
            "name": "Test Pricelist"
        })
        cls.sale_order = cls.env["sale.order"].create({
            "partner_id": cls.partner.id,
            "pricelist_id": cls.pricelist.id,
        })
        cls.sale_order_line = cls.env["sale.order.line"].create({
            "order_id": cls.sale_order.id,
            "product_id": cls.product.id,
            "product_uom_qty": 1,
            "price_unit": 100,
        })

    def test_compute_book_price(self):
        """Ensure book_price is computed correctly."""
        print("==============================1.==============================")
        self.sale_order_line._compute_book_price()
        expected_price = self.pricelist._get_product_price( self.product, 1, self.partner )

        self.assertEqual(self.sale_order_line.book_price, expected_price,)

    def test_prepare_invoice_line(self):
        print("==============================2.==============================")
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, "sale", 
        "Sale order should be confirmed.")

        invoice = self.sale_order._create_invoices()
        self.assertTrue(invoice, "Invoice should be created successfully.")

        invoice_line = invoice.invoice_line_ids.filtered(lambda line: line.product_id == self.product)
        self.assertTrue(invoice_line, "Invoice line should exist for the product.")

        '''Check if 'book_price' is copied correctly '''
        self.assertEqual(invoice_line.book_price, self.sale_order_line.book_price,
         "Book price should be correctly transferred to the invoice line.")
