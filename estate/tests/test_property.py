from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Création de deux propriétés de test
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Villa California',
                'living_area': 100,
                'garden_area': 50,
                'expected_price': 500000,
                'agency_id': cls.env.user.company_id.id,
            },
            {
                'name': 'Maison Paris',
                'living_area': 80,
                'garden_area': 20,
                'expected_price': 300000,
                'agency_id': cls.env.user.company_id.id,
            }
        ])

    def test_creation_area(self):
        """Test que le champ total_area est correctement calculé."""
        self.properties[0].living_area = 120
        self.properties[0].garden_area = 30
        self.properties[1].living_area = 60
        self.properties[1].garden_area = 40
        self.properties._compute_area()

        self.assertRecordValues(self.properties, [
           {'name': 'Villa California', 'total_area': 150},
           {'name': 'Maison Paris', 'total_area': 100},
        ])

    def test_action_sell(self):
        """Test le bon fonctionnement de la méthode de vente de propriété."""
        # On vend les propriétés
        self.properties[0].buyer_id = self.ref('base.res_partner_1')
        self.properties[1].buyer_id = self.ref('base.res_partner_1')
        self.properties.sell_property()

        self.assertRecordValues(self.properties, [
           {'name': 'Villa California', 'state': 'sold'},
           {'name': 'Maison Paris', 'state': 'sold'},
        ])

        # Vérifie qu'une UserError est levée si on tente une action interdite
        with self.assertRaises(UserError):
            self.properties.cancel_property()

    def test_garden_onchange_resets_fields(self):
        """Ensure that unchecking garden resets garden_area and garden_orientation."""
        property = self.env['estate.property'].create({
            'name': 'Test Garden Reset',
            'expected_price': 100000,
            'garden': True,
            'agency_id': self.env.user.company_id.id,
        })

        # Simulate the onchange manually
        property._onchange_garden()
        self.assertEqual(property.garden_area, 10)
        self.assertEqual(property.garden_orientation, 'north')

        # Uncheck the garden and simulate onchange again
        property.garden = False
        property._onchange_garden()
        self.assertEqual(property.garden_area, 0)
        self.assertFalse(property.garden_orientation)
