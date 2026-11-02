from odoo.tests import TransactionCase
from odoo.exceptions import UserError


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstatePropertyOfferTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([
            {'name':'P1', 'state':'new', 'expected_price':100000, 'selling_price':99000}
        ])
        cls.partner =  cls.env['res.partner'].create([{'name':'Partner 1'}])

    def test_create(self):
        """Test that everything behaves like it should when creating an offer on a property."""
        # Verify test preconditions
        self.assertRecordValues(self.properties, [{'name': 'P1', 'state': 'new'}])

        # Case: offer on a new property => OK
        offer = self.env['estate.property.offer'].create([{'property_id':self.properties.id, 'partner_id':self.partner.id, 'price': 99000}])
        self.assertRecordValues(offer, [{'status': None}])
        self.assertRecordValues(self.properties, [{'offer_ids': [offer.id]}])

        # Case: offer on a sold property => Error
        self.properties.state = 'sold' # enforce state
        with self.assertRaises(UserError, msg="Case: offer on a sold property"):
            self.env['estate.property.offer'].create([{'property_id':self.properties.id, 'partner_id':self.partner.id, 'price': 99900}])

        self.assertRecordValues(self.properties, [{'offer_ids': [offer.id]}])
