from odoo.tests import TransactionCase


class ModularTypeCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.mto_route = cls.env.ref("stock.route_warehouse0_mto")
        cls.manufacture_route = cls.env.ref("mrp.route_warehouse0_manufacture")

        cls.type_sections = cls.env["modular.type"].create({
            "name": "Sections"
        })
        cls.type_meters = cls.env["modular.type"].create({
            "name": "Meters"
        })

        cls.product = cls.env["product.template"].create({
            "name": "Test Fencing Product",
            "type": "consu",
            "modular_type_ids": [(6, 0, [
                cls.type_sections.id,
                cls.type_meters.id,
            ])],
            "route_ids": [(6, 0, [
                cls.mto_route.id,
                cls.manufacture_route.id,
            ])],
        })

        cls.product_no_modular = cls.env["product.template"].create({
            "name": "Normal Product",
            "type": "consu",
            "route_ids": [(6, 0, [
                cls.mto_route.id,
                cls.manufacture_route.id,
            ])],
        })

        cls.component_sections = cls.env["product.product"].create({
            "name": "Railing",
            "type": "consu",
        })
        cls.component_meters = cls.env["product.product"].create({
            "name": "Liner",
            "type": "consu",
        })
        cls.component_no_type = cls.env["product.product"].create({
            "name": "Screw",
            "type": "consu",
        })

        cls.bom = cls.env["mrp.bom"].create({
            "product_tmpl_id": cls.product.id,
            "product_qty": 1.0,
            "type": "normal",
            "bom_line_ids": [
                (0, 0, {
                    "product_id": cls.component_sections.id,
                    "product_qty": 5.0,
                    "modular_type_id": cls.type_sections.id,
                }),
                (0, 0, {
                    "product_id": cls.component_meters.id,
                    "product_qty": 2.0,
                    "modular_type_id": cls.type_meters.id,
                }),
                (0, 0, {
                    "product_id": cls.component_no_type.id,
                    "product_qty": 10.0,
                }),
            ],
        })

        cls.bom_no_modular = cls.env["mrp.bom"].create({
            "product_tmpl_id": cls.product_no_modular.id,
            "product_qty": 1.0,
            "type": "normal",
            "bom_line_ids": [
                (0, 0, {
                    "product_id": cls.component_no_type.id,
                    "product_qty": 10.0,
                }),
            ],
        })

        cls.customer = cls.env["res.partner"].create({
            "name": "Test Customer"
        })

    def _create_so(self, product_tmpl, qty=1.0, **values):
        """Helper — create a sale order with one line"""
        return self.env["sale.order"].create({
            "partner_id": self.customer.id,
            "order_line": [(0, 0, {
                "product_id": product_tmpl.product_variant_ids[0].id,
                "product_uom_qty": qty,
            })],
            **values,
        })

    def _get_mo(self, so, so_line):
        """Helper — fetch MO created from a confirmed SO line"""
        return self.env["mrp.production"].search([
            ("origin", "=", so.name),
            ("product_id", "=", so_line.product_id.id),
        ])
