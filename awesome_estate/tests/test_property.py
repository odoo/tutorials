from odoo.tests import TransactionCase, tagged


@tagged('standard')
class TestAwesomeEstateProperty(TransactionCase):
    """Test property lifecycle and business logic."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Property = cls.env['awesome.estate.property']
        cls.Offer = cls.env['awesome.estate.property.offer']
        cls.Maintenance = cls.env['awesome.estate.property.maintenance']
        cls.PropertyType = cls.env['awesome.estate.property.type']
        cls.PropertyTag = cls.env['awesome.estate.property.tag']
        cls.Partner = cls.env['res.partner']

        cls.partner_a = cls.Partner.create({'name': 'Buyer A'})
        cls.partner_b = cls.Partner.create({'name': 'Buyer B'})
        cls.type_house = cls.PropertyType.create({'name': 'House'})
        cls.tag_cozy = cls.PropertyTag.create({'name': 'Cozy', 'color': 4})

        cls.property = cls.Property.create(
            {
                'name': 'Test Villa',
                'expected_price': 500000,
                'property_type_id': cls.type_house.id,
                'tag_ids': [(6, 0, [cls.tag_cozy.id])],
                'bedrooms': 3,
                'living_area': 150,
                'garden': True,
                'garden_area': 50,
            }
        )

    def test_property_default_state(self):
        self.assertEqual(self.property.state, 'new')
        self.assertTrue(self.property.active)
        self.assertEqual(self.property.bedrooms, 3)

    def test_compute_total_area(self):
        self.assertEqual(self.property.total_area, 200)

    def test_compute_best_price_no_offers(self):
        self.assertEqual(self.property.best_price, 0.0)

    def test_garden_onchange(self):
        self.property.garden = False
        self.property._onchange_garden()
        self.assertEqual(self.property.garden_area, 0)
        self.assertFalse(self.property.garden_orientation)

        self.property.garden = True
        self.property._onchange_garden()
        self.assertEqual(self.property.garden_area, 10)
        self.assertEqual(self.property.garden_orientation, 'north')

    def test_create_offer_moves_to_offer_received(self):
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        self.assertEqual(self.property.state, 'offer_received')

    def test_offer_price_must_escalate(self):
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        with self.assertRaises(Exception):
            self.Offer.create(
                {
                    'property_id': self.property.id,
                    'partner_id': self.partner_b.id,
                    'price': 400000,
                }
            )

    def test_accept_offer_sets_selling_price(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        offer.action_accept()
        self.assertEqual(self.property.state, 'offer_accepted')
        self.assertEqual(self.property.selling_price, 450000)
        self.assertEqual(self.property.buyer_id, self.partner_a)

    def test_accept_best_offer(self):
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_b.id,
                'price': 480000,
            }
        )
        self.property.action_accept_best_offer()
        self.assertEqual(self.property.selling_price, 480000)
        self.assertEqual(self.property.state, 'offer_accepted')

    def test_cancel_property_refuses_pending_offers(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        self.property.action_cancel()
        self.assertEqual(self.property.state, 'canceled')
        self.assertFalse(self.property.active)
        self.assertEqual(offer.status, 'refused')

    def test_reset_sold_property(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        offer.action_accept()
        self.property.action_sold()
        self.property.action_reset()
        self.assertEqual(self.property.state, 'new')
        self.assertEqual(self.property.selling_price, 0.0)
        self.assertFalse(self.property.buyer_id)
        self.assertTrue(self.property.active)

    def test_delete_only_new_or_canceled(self):
        with self.assertRaises(Exception):
            self.property.state = 'sold'
            self.property.unlink()

    def test_cannot_delete_sold(self):
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        offer.action_accept()
        self.property.action_sold()
        with self.assertRaises(Exception):
            self.property.unlink()

    def test_selling_price_90_percent_rule(self):
        """Selling price must be >= 90% of expected price."""
        offer = self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 450000,
            }
        )
        offer.action_accept()
        self.assertEqual(self.property.selling_price, 450000)

    def test_suspicious_offer_count(self):
        dup_partner = self.Partner.create({'name': 'Dup Buyer'})
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': dup_partner.id,
                'price': 400000,
            }
        )
        self.Offer.create(
            {
                'property_id': self.property.id,
                'partner_id': dup_partner.id,
                'price': 410000,
            }
        )
        self.assertGreater(self.property.suspicious_offer_count, 0)

    def test_cron_archive_stale_properties(self):
        self.Property._cron_archive_stale_properties()

    def test_cron_remind_expiring_offers(self):
        self.Property._cron_remind_expiring_offers()
