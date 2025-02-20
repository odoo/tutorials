from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, Form, TransactionCase


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()
        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.property = cls.env["estate.property"].create(
            [{"name": "Property 1", "status": "new", "expected_price": 10}]
        )

        cls.property_test= cls.env["estate.property"].create(
            [{"name": "Demo Property", "status": "new", "expected_price": 100}]
        )

        cls.partner_id = cls.env["res.partner"].create({"name": "Demo Partner"})

        cls.offer1 = cls.env["estate.property.offer"].create(
            [
                {
                    "property_id": cls.property.id,
                    "partner_id": cls.partner_id.id,
                    "price": 1000,
                    "status_offer": "accepted",
                }
            ]
        )

        cls.offer2 = cls.env["estate.property.offer"].create(
            [
                {
                    "property_id": cls.property_test.id,
                    "partner_id": cls.partner_id.id,
                    "price": 1000,
                    "status_offer": "accepted",
                }
            ]
        )
        cls.offer2.accept_offer()

    # def test_sell_a_property_with_no_accepted_offers(self):
    #     with self.assertRaises(UserError):
    #         self.property.action_sold()

    def test_create_offer_for_a_sold_property(self):
        print(
            "-------------------------------1------------------------------------------"
        )
        #self.property.status = "sold"
        self.property_test.sold_event()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "property_id": self.property_test.id,
                        "partner_id": self.partner_id.id,  # change
                        "price": 20000,
                    }
                ]
            )

    def test_sell_a_property_with_no_accepted_offers(self):
        print(
            "------------------------------2-----------------------------------------"
        )
        self.offer1.status_offer = "refused"
        with self.assertRaises(UserError):
            self.property.sold_event()

    def test_sold_is_correctly_marked(self):
        print(
            "------------------------------3-----------------------------------------"
        )
        print(self.property.status)
        self.offer1.accept_offer()
        print(self.property.status)
        self.property.sold_event()
        self.assertEqual(
            self.property.status,
            "sold",
            "Property Should be marked as sold after selling it",
        )

    def test_garden_onchange_reset_and_resotre(self):
        print(
            "------------------------------4-----------------------------------------"
        )
        estate_form = Form(self.property)
        estate_form.garden = True
        self.assertEqual(estate_form.garden_area, 1000)
        self.assertEqual(estate_form.garden_orientation, "north")
        print("CHECK TEST CASE IS PASSED!")
        print(estate_form.garden_area, " ", estate_form.garden_orientation)
        estate_form.garden = False
        self.assertEqual(estate_form.garden_area, 0)
        self.assertEqual(estate_form.garden_orientation, False)
        print("===" * 50)
        print("UNCHECK TEST CASE IS PASSED!")
        print(estate_form.garden_area, " ", estate_form.garden_orientation)
