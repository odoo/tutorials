from odoo.tests import tagged
from odoo.tests.common import TransactionCase


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.property_a = cls.env["estate_property"].create(
            {
                "name": "property",
                "expected_price": "250000",
            },
        )

        cls.buyer_a = cls.env["res.partner"].create({"name": "buyer_a"})

        cls.buyer_b = cls.env["res.partner"].create({"name": "buyer_b"})

        cls.offer_a = cls.env["estate_property.offer"].create(
            {
                "name": "offer_a",
                "price": "245000",
                "partner_id": cls.buyer_a,
                "property_id": cls.property_a,
            },
        )

        cls.offer_b = cls.env["estate_property.offer"].create(
            {
                "name": "offer_b",
                "price": "267000",
                "partner_id": cls.buyer_b,
                "property_id": cls.property_a,
            },
        )

        def test_accept_offer(self):
            """Test that the action of accepting an offer behaves like it should"""

            self.assertRecordValues(self.property_a, [{"offer_ids": {}}])

            offer_a = self.env["estate_property.offer"].create(
                {
                    "name": "offer_a",
                    "price": "245000",
                    "partner_id": cls.buyer_a,
                    "property_id": cls.property_a,
                },
            )

            offer_b = self.env["estate_property.offer"].create(
                {
                    "name": "offer_b",
                    "price": "267000",
                    "partner_id": cls.buyer_b,
                    "property_id": cls.property_a,
                },
            )

            self.assertRecordValues(
                self.property_a,
                [
                    {
                        "offer_ids": {offer_a.id, offer_b.id},
                    },
                ],
            )

            self.offer_b.accept_offer_action()

            self.assertRecordValues(
                offer_b,
                [
                    {
                        "status": "accepted",
                    },
                ],
            )

            self.assertRecordValues(
                self.property_a,
                [
                    {
                        "buyer": offer_b.partner_id,
                        "selling_price": offer_b.price,
                    },
                ],
            )
