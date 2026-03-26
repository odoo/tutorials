import datetime

from odoo.addons.base.tests.common import BaseCommon


class EstateTestCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Test Partner A',
        })

        cls.property_type_house = cls.env['estate.property.type'].create({
            'name': 'House',
        })
        cls.property_type_apartment = cls.env['estate.property.type'].create({
            'name': 'Apartment',
        })

    def get_create_property_kwargs(self, **kwargs):
        return {
            'name': 'Property ' + str(datetime.datetime.now()),
            'postcode': '12345',
            'date_availability': datetime.datetime.now() + datetime.timedelta(days=7),
            'expected_price': 100000,
            'bedrooms': 2,
            'living_area': 120,
            'facades': 2,
            'property_type_id': self.property_type_house.id,
            'state': 'new',
            **kwargs,
        }

    def create_property(self, state, **kwargs):
        estate_property = self.env['estate.property'].create(self.get_create_property_kwargs(**kwargs))

        if state in {'offer_received', 'offer_accepted', 'sold', 'canceled'}:
            offer_a = self.create_offer(estate_property, 5000, partner_id=self.partner.id, validity=7)
            offer_b = self.create_offer(estate_property, 10000, partner_id=self.partner_a.id, validity=14)

        if state in {'offer_accepted', 'sold'}:
            offer_a.action_mark_as_refused()
            offer_b.action_mark_as_accepted()

        if state == 'sold':
            estate_property.action_mark_as_sold()
        elif state == 'canceled':
            estate_property.action_mark_as_canceled()

        return estate_property

    def create_offer(self, estate_property, price_increase=0, **kwargs):
        return self.env['estate.property.offer'].create({
            'price': estate_property.expected_price + price_increase,
            'partner_id': self.partner.id,
            'property_id': estate_property.id,
            'validity': 7,
            **kwargs,
        })
