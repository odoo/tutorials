from odoo import Command
from odoo.tests.common import tagged, TransactionCase


@tagged('post_install', '-at_install', 'test_mod_types')
class TestModularTypes(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env['ir.config_parameter'].set_param('stock.picking_type_use_existing_location', True)
        mto_route = self.env.ref('stock.route_warehouse0_mto')
        mto_route.active = True
        
        self.modular_type_section = self.env['modular.types'].create({
            'name': 'Section',
            'multiplier': 1,
        })
        self.modular_type_meters = self.env['modular.types'].create({
            'name': 'Meters',
            'multiplier': 1,
        })

        self.component_1 = self.env['product.template'].create({
            'name': 'Component 1',
            'type': 'consu',
        })

        self.component_2 = self.env['product.template'].create({
            'name': 'Component 2',
            'type': 'consu',
        })

        manufacture_route = self.env['stock.route'].search([('name', '=', 'Manufacture')])
        mto_route = self.env['stock.route'].search([('name', '=', 'Replenish on Order (MTO)')])

        self.product_tmpl = self.env['product.template'].create({
            'name': 'Main Product',
            'type': 'consu',
            'route_ids': [
                Command.link(manufacture_route.id),
                Command.link(mto_route.id)
            ],
            'modular_type_ids': [
                Command.link(self.modular_type_section.id),
                Command.link(self.modular_type_meters.id)
            ]
        })
        self.product = self.product_tmpl.product_variant_id

        self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_tmpl.id,
            'bom_line_ids': [
                Command.create({
                    'product_id': self.component_1.id,
                    'product_qty': 1,
                    'modular_type_id': self.modular_type_section.id
                }),
                Command.create({
                    'product_id': self.component_2.id,
                    'product_qty': 1,
                    'modular_type_id': self.modular_type_meters.id
                })
            ]
        })

    def test_modular_types(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id
        })

        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product.id,
            'product_uom_qty': 1,
        })

        wizard = self.env['modular.types.wizard'].with_context(active_id=sale_order_line.id).create({})

        for line in wizard.modular_wizard_line_ids:
            if line.modular_type_id == self.modular_type_section:
                line.current_value = 3
            elif line.modular_type_id == self.modular_type_meters:
                line.current_value = 4

        wizard.action_add_modular_values()

        sale_order.action_confirm()

        mo = self.env['mrp.production'].search([('origin', '=', sale_order.name)], limit=1)
        for line in mo.move_raw_ids:
            if line.product_id == self.component_1:
                self.assertEqual(line.product_uom_qty, 3, "Component 1 quantity should be multiplied by 3")
            elif line.product_id == self.component_2:
                self.assertEqual(line.product_uom_qty, 4, "Component 2 quantity should be multiplied by 4")

        self.assertEqual(self.modular_type_section.multiplier, 3, "Section multiplier should be updated to 3")
        self.assertEqual(self.modular_type_meters.multiplier, 4, "Meters multiplier should be updated to 4")
