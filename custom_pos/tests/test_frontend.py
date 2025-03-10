from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestCustomPos(TestPointOfSaleHttpCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.test_product = cls.env['product.product'].create({
            'name': 'Acoustic Bloc Screens (Wood)',
            'type': 'consu',
            'available_in_pos': True,
            'barcode': '6016478556530',
            'list_price': 100.0,
            'custom_price': 80.0,
            'taxes_id': [(6, 0, [])],
            'min_price': 50.0
        })

    def test_custom_pos_tour_suite(self):
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_tour(f"/pos/ui?config_id={self.main_pos_config.id}", 'TicketScreenBarcodeSearch', login="pos_user")
        self.start_tour(f"/pos/ui?config_id={self.main_pos_config.id}", 'OrderWidgetMinPricePopUp', login="pos_user")
