from odoo.tests import tagged
from .common import ModularTypeCommon


@tagged("post_install", "-at_install", "modular_type")
class TestModularType(ModularTypeCommon):

    def test_01_modular_values_applied_to_mo(self):
        so = self._create_so(self.product)
        so_line = so.order_line[0]

        so_line.write({
            "modular_value_ids": [
                (0, 0, {
                    "modular_type_id": self.type_sections.id,
                    "value": 6.0,
                }),
                (0, 0, {
                    "modular_type_id": self.type_meters.id,
                    "value": 3.0,
                }),
            ]
        })

        so.action_confirm()
        so_line._apply_modular_values_to_productions()

        mo = self._get_mo(so, so_line)
        self.assertTrue(mo, "MO should be created after SO confirm")

        for move in mo.move_raw_ids:
            if move.bom_line_id.modular_type_id == self.type_sections:
                self.assertEqual(
                    move.product_uom_qty, 30.0,
                    "Sections: 5 × 6 = 30"
                )
            elif move.bom_line_id.modular_type_id == self.type_meters:
                self.assertEqual(
                    move.product_uom_qty, 6.0,
                    "Meters: 2 × 3 = 6"
                )

    def test_02_no_values_set_qty_is_zero(self):
        so = self._create_so(self.product)
        so_line = so.order_line[0]

        self.assertFalse(
            so_line.modular_value_ids,
            "No modular values should be set"
        )

        so.action_confirm()
        so_line._apply_modular_values_to_productions()

        mo = self._get_mo(so, so_line)
        self.assertTrue(mo, "MO should still be created")

        for move in mo.move_raw_ids.filtered(
            lambda m: m.bom_line_id.modular_type_id
        ):
            self.assertEqual(
                move.product_uom_qty, 0.0,
                f"{move.product_id.name} qty should be 0 when no values set"
            )

    def test_03_no_modular_type_standard_qty(self):
        so = self._create_so(self.product_no_modular, qty=2.0)
        so_line = so.order_line[0]

        so.action_confirm()

        so_line._apply_modular_values_to_productions()

        mo = self._get_mo(so, so_line)
        self.assertTrue(mo, "MO should be created")

        for move in mo.move_raw_ids:
            self.assertEqual(
                move.product_uom_qty, 20.0,
                "Standard product should follow normal qty calculation"
            )
