from odoo import Command
from odoo.tests.common import TransactionCase, tagged
from odoo.tools import float_is_zero
from odoo.tools.float_utils import float_compare


@tagged('post_install', '-at_install')
class ModularTypesTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Unarchive MTO route
        cls.route_mto = cls.env.ref('stock.route_warehouse0_mto')
        cls.route_mto.write({'active': True})
        cls.route_manufacture = cls.env.ref('mrp.route_warehouse0_manufacture')

        # Create modular types
        cls.modular_type_seats = cls.env['product.modular.type'].create({
            'name': 'Seats'
        })
        cls.modular_type_size = cls.env['product.modular.type'].create({'name': 'Size'})
        cls.modular_type_storage = cls.env['product.modular.type'].create({
            'name': 'Storage'
        })
        cls.modular_type_unused = cls.env['product.modular.type'].create({
            'name': 'Unused'
        })

        # Create a table set product with MTO routes and Modular types set
        cls.product_table = cls.env['product.product'].create({
            'name': 'Modular Table Set',
            'type': 'consu',
            'tracking': 'none',
            'modular_type_ids': [
                Command.set([
                    cls.modular_type_seats.id,
                    cls.modular_type_size.id,
                    cls.modular_type_storage,
                ])
            ],
            'route_ids': [Command.set([cls.route_mto.id, cls.route_manufacture.id])],
        })

        # Create components
        cls.product_chair = cls.env.ref('product.product_product_12')
        cls.product_drawer = cls.env.ref('product.product_product_27')
        cls.product_table_top = cls.env.ref('mrp.product_product_computer_desk_head')
        cls.product_table_leg = cls.env.ref('mrp.product_product_computer_desk_leg')

        # Create BOM
        cls.bom = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.product_table.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                Command.create({
                    'product_id': cls.product_table_top.id,
                    'product_qty': 1.0,
                    'modular_type_id': cls.modular_type_size.id,
                }),
                Command.create({
                    'product_id': cls.product_table_leg.id,
                    'product_qty': 4.0,
                }),
                Command.create({
                    'product_id': cls.product_chair.id,
                    'product_qty': 1.0,
                    'modular_type_id': cls.modular_type_seats.id,
                }),
                Command.create({
                    'product_id': cls.product_drawer.id,
                    'product_qty': 1.0,
                    'modular_type_id': cls.modular_type_storage.id,
                }),
            ],
        })

        cls.customer = cls.env.ref('base.res_partner_2')
        cls.product_normal = cls.env.ref('product.product_product_11')
        cls.product_normal.route_ids = [
            Command.set([cls.route_mto.id, cls.route_manufacture.id])
        ]

    def test_normal_product(self):
        """Test that a normal product can be sold and manufactured"""

        sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'order_line': [
                Command.create({
                    'product_id': self.env.ref('product.product_product_11'),
                    'product_uom_qty': 3.0,
                })
            ],
        })

        sale_order.action_confirm()

        self.assertEqual(
            len(sale_order.mrp_production_ids),
            1,
            'One manufacturing order should be created',
        )

        self.assertEqual(
            sale_order.mrp_production_ids.product_id,
            self.product_normal,
            'Manufacturing order should have the correct product',
        )
        self.assertEqual(
            sale_order.mrp_production_ids.state,
            'confirmed',
            'Manufacturing order should be in confirmed state',
        )

    def test_modular_product_complete_workflow(self):
        """Test the complete modular type workflow and verify MO quantities"""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'order_line': [
                Command.create({
                    'product_id': self.product_table.id,
                    'product_uom_qty': 2.0,
                })
            ],
        })

        so_line = sale_order.order_line[0]

        # Create modular type values
        self.env['modular.type.value'].create({
            'sale_order_line_id': so_line.id,
            'modular_type_id': self.modular_type_size.id,
            'value': 2.0,
        })

        self.env['modular.type.value'].create({
            'sale_order_line_id': so_line.id,
            'modular_type_id': self.modular_type_seats.id,
            'value': 5.0,
        })

        sale_order.action_confirm()

        self.assertEqual(
            len(sale_order.mrp_production_ids),
            1,
            'One manufacturing order should be created',
        )

        mo = sale_order.mrp_production_ids[0]

        self.assertTrue(
            mo.is_modular_bom, 'Manufacturing order should be marked as modular'
        )

        # Check component quantities in the MO
        top_move = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_table_top
        )
        chair_move = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_chair
        )
        legs_move = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_table_leg
        )
        drawer_move = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_drawer
        )

        self.assertEqual(
            float_compare(top_move.product_uom_qty, 2.00, 2),
            0,
            'Table top quantity should be multiplied by length value',
        )

        self.assertEqual(
            float_compare(chair_move.product_uom_qty, 5.00, 2),
            0,
            'Chair quantity should be multiplied by seats value',
        )

        self.assertTrue(
            float_is_zero(drawer_move.product_uom_qty, 2), 'Drawer quantity should be 0'
        )

        self.assertEqual(
            float_compare(legs_move.product_uom_qty, 4.00, 2),
            0,
            'Legs quantity should remain the same',
        )

    def test_modular_product_without_values(self):
        """Test creating SO with modular product but without setting modular type values"""
        sale_order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'order_line': [
                Command.create({
                    'product_id': self.product_table.id,
                    'product_uom_qty': 5.0,
                })
            ],
        })

        sale_order.action_confirm()

        self.assertEqual(
            len(sale_order.mrp_production_ids),
            1,
            'One manufacturing order should be created',
        )

        mo = sale_order.mrp_production_ids[0]
        top_qty = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_table_top
        ).product_uom_qty
        legs_qty = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_table_leg
        ).product_uom_qty
        chair_qty = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_chair
        ).product_uom_qty
        drawer_qty = mo.move_raw_ids.filtered(
            lambda m: m.product_id == self.product_drawer
        ).product_uom_qty

        # When no values are set, the default modular factor should be 0,
        # so the modular component quantities should be 0
        self.assertTrue(
            float_is_zero(top_qty, 2),
            'Table top quantity should be 0 when no modular values are set',
        )
        self.assertTrue(
            float_is_zero(chair_qty, 2),
            'Chair quantity should be 0 when no modular values are set',
        )
        self.assertTrue(
            float_is_zero(drawer_qty, 2),
            'Drawer quantity should be 0 when no modular values are set',
        )

        # The legs quantity should remain the same (4 legs per table)
        self.assertEqual(
            float_compare(legs_qty, 4.0, 2), 0, 'Legs quantity should remain unchanged'
        )
