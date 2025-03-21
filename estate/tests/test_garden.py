#type:ignore
from .test_common import EstateTestCommon


class TestEstatePropertyGarden(EstateTestCommon):

    def test_garden_reset_on_uncheck(self):
        """Ensure garden area and orientation reset when garden is unchecked."""
        self.property.garden = True
        self.property.garden_area = 50
        self.property.garden_orientation = 'north'

        self.property.garden = False

        self.assertEqual(self.property.garden_area, 0, "Garden area should reset to 0.")
        self.assertFalse(self.property.garden_orientation, "Garden orientation should reset.")
