from odoo.tests.common import TransactionCase


class EstateTestCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Buyer',
            'email': 'buyer@example.com',
        })

        cls.property_type = cls.env['estate.property.type'].search([('name', '=', "House")])

        cls.tag1 = cls.env['estate.property.tag'].create({'name': 'Luxury'})
        cls.tag2 = cls.env['estate.property.tag'].create({'name': 'Garden'})

        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Cozy Cottage',
                'expected_price': 250000,
                'property_type_id': cls.property_type.id,
                'description': 'A beautiful cottage in the countryside.',
                'postcode': '12345',
                'living_area': 120,
                'facades': 2,
                'garage': True,
                'garden': True,
                'garden_area': 20,
                'garden_orientation': "north",
                'bedrooms': 3,
                'buyer_id': cls.partner.id,
                'tag_ids': [(6, 0, [cls.tag1.id, cls.tag2.id])],
            },
            {
                'name': 'Modern Apartment',
                'expected_price': 180000,
                'property_type_id': cls.property_type.id,
                'description': 'City center apartment with modern design.',
                'postcode': '54321',
                'living_area': 85,
                'facades': 1,
                'garage': False,
                'garden': False,
                'bedrooms': 2,
                'tag_ids': [(6, 0, [cls.tag1.id])],
            },
            {
                'name': 'Beachfront Villa',
                'expected_price': 750000,
                'property_type_id': cls.property_type.id,
                'description': 'Villa with private beach access.',
                'postcode': '67890',
                'living_area': 200,
                'facades': 4,
                'garage': True,
                'garden': True,
                'garden_area': 100,
                'bedrooms': 5,
                'tag_ids': [(6, 0, [cls.tag2.id])],
            },
        ])

        # Create offers for only 2 properties (leave one without offers)
        cls.offers = cls.env['estate.property.offer'].create([
            {
                'price': 260000,
                'partner_id': cls.partner.id,
                'property_id': cls.properties[0].id,  # Cozy Cottage
            },
            {
                'price': 185000,
                'partner_id': cls.partner.id,
                'property_id': cls.properties[1].id,  # Modern Apartment
            },
            # No offer for Beachfront Villa -> will trigger UserError when trying to sell
        ])
