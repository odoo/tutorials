from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstatePropertyTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([{'name': 'P1', 'state': 'new', 'expected_price': 100000}])
        cls.partner = cls.env['res.partner'].create([{'name': 'Partner 1'}])

    def test_action_property_sold(self):
        """Test that everything behaves like it should when selling a property."""
        # Case: no offer yet => error
        with self.assertRaises(UserError):
            self.properties.action_property_sold()

        # Case: One offer but not yet accepted => error
        self.assertRecordValues(self.properties, [{'name': 'P1', 'state': 'new'}])
        offer = self.env['estate.property.offer'].create(
            [{'property_id': self.properties.id, 'partner_id': self.partner.id, 'price': 99000}])
        self.assertRecordValues(offer, [{'status': None}])
        self.properties.offer_ids = [offer.id]
        with self.assertRaises(UserError, msg="Case: One offer but not yet accepted"):
            self.properties.action_property_sold()

        # Case: One offer accepted => OK
        offer.action_accept_property_offer()
        self.assertRecordValues(self.properties, [
            {'name': 'P1', 'state': 'offer_accepted'}])
        self.properties.action_property_sold()
        self.assertRecordValues(self.properties, [
            {'name': 'P1', 'state': 'sold'}
        ])

    def test_estate_property_view_form(self):
        """ Property View Form-test. """
        property_view_form = Form(self.env['estate.property'])
        self.assertEqual(property_view_form.garden_area, 0)
        self.assertFalse(property_view_form.garden_orientation)
        self.assertFalse(property_view_form.garden)

        property_view_form.garden = True
        self.assertEqual(property_view_form.garden_area, 10)
        self.assertEqual(property_view_form.garden_orientation, 'north')

        property_view_form.garden = False
        self.assertEqual(property_view_form.garden_area, 0)
        self.assertFalse(property_view_form.garden_orientation)
