from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, TransactionCase
from odoo.tools import mute_logger


class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})
        cls.property_type = cls.env['estate.property.type'].create({
            'name': 'Test Property Type'
        })
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property 1',
            'property_type_id': cls.property_type.id,
            'expected_price': 100000,
        })

    def test_total_area_computing(self):

        self.assertRecordValues(self.property, [
           {'name': 'Test Property 1', 'total_area': 0}
        ])

        self.property.living_area = 0
        self.assertRecordValues(self.property, [
           {'name': 'Test Property 1', 'total_area': 0}
        ])

        self.property.living_area = 20
        self.assertRecordValues(self.property, [
           {'name': 'Test Property 1', 'total_area': 20}
        ])

        self.property.living_area = 0
        self.property.garden = True
        self.property.garden_area = 10
        self.assertRecordValues(self.property, [
           {'name': 'Test Property 1', 'total_area': 10}
        ])

        self.property.living_area = 20
        self.property.garden = True
        self.property.garden_area = 10
        self.assertRecordValues(self.property, [
           {'name': 'Test Property 1', 'total_area': 30}
        ])

    def test_best_price_computing(self):
        """Should choose the maximum best price offer"""

        #No offers, best price is 0
        self.assertRecordValues(self.property, [
           {'name': 'Test Property 1', 'best_price': 0}
        ])
        # one offer, this becomes best price
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 100000,
            'partner_id': self.partner.id
        })
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 1', 'best_price': 100000}
        ])
        # second offer, best price is highest
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 100,
            'partner_id': self.partner.id
        })
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 1', 'best_price': 100000}
        ])
        # 10 offers, highest is best
        for i in range(10):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 105000 - i * 1000,
                'partner_id': self.partner.id
            })
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 1', 'best_price': 105000}
        ])
        # remove an offer that is not the highest, highest stays. Keep 104000
        self.env['estate.property.offer'].search([('property_id', '=', self.property.id), ('price', '=', 102000)]).unlink()
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 1', 'best_price': 105000}
        ])
        # remove the highest offer, best price updates
        self.env['estate.property.offer'].search([('property_id', '=', self.property.id), ('price', '=', 105000)]).unlink()
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 1', 'best_price': 104000}
        ])
        # remove all offers, best price becomes 0
        self.env['estate.property.offer'].search([('property_id', '=', self.property.id)]).unlink()
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 1', 'best_price': 0}
        ])

    #FORM

    def test_creation_required_fields_name_and_property_type(self):
        new_property = Form(self.env['estate.property'])
        new_property.expected_price = 100000
        with self.assertRaises(AssertionError):
            new_property.save()
        new_property.name = 'Test House from Form'
        with self.assertRaises(AssertionError):
            new_property.save()
        new_property.property_type_id = self.property_type
        new_property.save() # should not raise error

    def test_creation_expected_price_must_be_strictly_positive(self):
        existing_property = Form(self.property)

        for invalid_price in (-100000, 0, 0.0001): #0.0001 is lower than espilon for currency value
            with self.subTest(msg=f"Invalid price: {invalid_price}", invalid_price=invalid_price):
                existing_property.expected_price = invalid_price
                with self.assertRaisesRegex(Exception, 'estate_property_positive_expected_price'), mute_logger('odoo.sql_db'):
                    with self.cr.savepoint():
                        existing_property.save()

        existing_property.expected_price = 0.001 #0.001 is just enough to be higher than 0. Will still be displayed as 0 however.
        existing_property.save()
        self.assertEqual(self.property.expected_price, 0.001)

    def test_action_cannot_offer_when_property_is_sold(self):
        """Test that a sold property cannot be offered."""
        self.property.state = 'sold'

        offer = Form(self.env['estate.property.offer'])
        offer.price = 100000
        offer.partner_id = self.env['res.partner'].create({'name': 'Test Partner'})
        offer.property_id = self.property
        with self.assertRaises(UserError):
            offer.save()

    def test_action_cannot_offer_negative_or_zero_price(self):
        """Test that offering a negative or zero price throws an error."""
        partner = self.env['res.partner'].create({'name': 'Test Partner'})

        offer = Form(self.env['estate.property.offer'])
        offer.price = -100000
        offer.partner_id = partner
        offer.property_id = self.property
        for negative_offer_price in (-10000,-0.001, 0, 0.000499999):
            with self.subTest(msg=f"Invalid price: {negative_offer_price}", negative_offer_price=negative_offer_price):
                offer.price = negative_offer_price
                with self.assertRaisesRegex(Exception, 'estate_property_offer_check_price'), mute_logger('odoo.sql_db'):
                    with self.cr.savepoint():
                        offer.save()
        offer.price = 0.0005
        offer.save()

    def test_action_sold_property_is_marked_as_sold(self):
        """Test that selling a property marks it as sold."""
        partner = self.env['res.partner'].create({'name': 'Test Buyer'})

        # Ensure the offer price is >= 90% of expected_price so validation passes
        offer = self.env['estate.property.offer'].create({
            'price': self.property.expected_price,
            'partner_id': partner.id,
            'property_id': self.property.id,
        })

        # Accept the offer (should sets buyer_id & selling_price)
        offer.action_accept_offer()

        # Trigger the "Mark as Sold" button action
        self.property.action_sold()

        # Verify the property state and related fields
        self.assertEqual(self.property.state, 'sold')
        self.assertEqual(self.property.buyer_id, partner)
        self.assertEqual(self.property.selling_price, self.property.expected_price)

    def test_action_offer_price_below_90percent_throws(self):
        """Test that offering a price below 90% of expected price throws an error."""
        partner = self.env['res.partner'].create({'name': 'Test Buyer'})

        self.property.expected_price = 10000 # when we test a specific value, it's better to have it on hand rather than having it far away in setup

        # Create an offer with a price below 90% of expected price
        offer = self.env['estate.property.offer'].create({
            'price': 8000, #use specific value rather than depending on float's inaccurate multiplication
            'partner_id': partner.id,
            'property_id': self.property.id,
        })

        with self.assertRaises(UserError):
            offer.action_accept_offer()

        offer.price = 8999.99 #Close but not enough
        with self.assertRaises(UserError):
            offer.action_accept_offer()

        offer.price = 8999.999 #should not round at 3 digits (unless ? accounting policy is usually to have 3 digits for monetary values but I'm not sure)
        with self.assertRaises(UserError):
            offer.action_accept_offer()

        offer.price = 8999.9994999 #should not round up yet
        with self.assertRaises(UserError):
            offer.action_accept_offer()

        offer.price = 8999.9995 #ought to round up therefore should be ok
        offer.action_accept_offer()
