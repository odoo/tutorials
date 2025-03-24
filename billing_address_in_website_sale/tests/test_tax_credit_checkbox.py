import odoo.tests


@odoo.tests.tagged("post_install", "-at_install")
class TestTaxCreditCheckbox(odoo.tests.HttpCase):
    def test_tax_credit_checkbox_flow(self):
        self.env["product.product"].create(
            {
                "name": "Office Chair Black TEST",
                "list_price": 12.50,
            }
        )

        self.start_tour("/", "tax_credit_checkbox_test", login="admin")
