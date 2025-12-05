from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError
from odoo import Command, fields


@tagged('post_install', '-at_install')
class TestSimplifiedRoutes(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.buy_route = cls.env.ref('purchase_stock.route_warehouse0_buy')
        cls.mfg_route = cls.env.ref('mrp.route_warehouse0_manufacture')
        cls.subcontract_route = cls.env.ref('mrp_subcontracting.route_resupply_subcontractor_mto')
        cls.dropship_route = cls.env.ref('stock_dropshipping.route_drop_shipping')
        cls.dropship_subcontractor_route = cls.env.ref('mrp_subcontracting_dropshipping.route_subcontracting_dropshipping')

        cls.vendor = cls.env['res.partner'].create({
            'name': 'Test Vendor',
            'email': 'vendor@test.com',
        })

        cls.categ_all = cls.env.ref('product.product_category_all')

        cls.finished_product = cls.env['product.template'].create({
            'name': 'Finished Product',
            'type': 'consu',
            'categ_id': cls.categ_all.id,
            'purchase_ok': True,
            'sale_ok': True,
        })

        cls.component_product = cls.env['product.template'].create({
            'name': 'Component Product',
            'type': 'consu',
            'categ_id': cls.categ_all.id,
            'purchase_ok': True,
            'sale_ok': True,
        })

        cls.env['product.supplierinfo'].create({
            'partner_id': cls.vendor.id,
            'product_tmpl_id': cls.component_product.id,
            'price': 10.0,
        })

        cls.subcontractor = cls.env['res.partner'].create({
            'name': 'Test Subcontractor',
            'email': 'subcontractor@test.com',
        })

    def test_01_buy_route_auto_assignment(self):
        """Test automatic Buy route assignment based on purchase_ok flag"""
        self.assertIn(self.buy_route.id, self.finished_product.route_ids.ids,
                      "Buy route should be automatically assigned when purchase_ok is True")

        self.finished_product.write({'purchase_ok': False})

        self.assertNotIn(self.buy_route.id, self.finished_product.route_ids.ids,
                         "Buy route should be automatically removed when purchase_ok is False")


        self.finished_product.write({'purchase_ok': True})

        self.assertIn(self.buy_route.id, self.finished_product.route_ids.ids,
                      "Buy route should be automatically re-assigned when purchase_ok is True")

    def test_02_manufacture_route_auto_assignment(self):
        """Test automatic Manufacture route assignment based on BOM existence"""
        self.assertNotIn(self.mfg_route.id, self.finished_product.route_ids.ids,
                         "Manufacture route should not be assigned when no BOM exists")

        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [
                Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        self.assertIn(self.mfg_route.id, self.finished_product.route_ids.ids,
                      "Manufacture route should be automatically assigned when a BOM exists")

        bom.unlink()

        self.assertNotIn(self.mfg_route.id, self.finished_product.route_ids.ids,
                         "Manufacture route should be automatically removed when BOM is deleted")

    def test_03_subcontract_route_auto_assignment(self):
        """Test automatic Subcontract route assignment for components in subcontracting BOMs"""
        self.assertNotIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                         "Subcontract route should not be assigned when component is not used in subcontracting BOM")

        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.id,
            'product_qty': 1.0,
            'type': 'subcontract',
            'subcontractor_ids': [Command.link(self.subcontractor.id)],
            'bom_line_ids': [Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        self.assertIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                      "Subcontract route should be automatically assigned to component used in subcontracting BOM")

        bom.unlink()

        self.assertNotIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                         "Subcontract route should be automatically removed when subcontracting BOM is deleted")

    def test_04_dropship_functionality(self):
        """Test regular dropship functionality"""

        self.finished_product.write({'route_ids': [Command.link(self.dropship_route.id)]})

        self.assertIn(self.dropship_route.id, self.finished_product.route_ids.ids,
                      "Dropship route should be assigned")

        self.assertNotIn(self.dropship_subcontractor_route.id, self.finished_product.route_ids.ids,
                         "Dropship subcontractor route should not be assigned to non-component products")

    def test_05_dropship_subcontractor_functionality(self):
        """Test dropship subcontractor functionality"""

        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.id,
            'product_qty': 1.0,
            'type': 'subcontract',
            'subcontractor_ids': [Command.link(self.subcontractor.id)],
            'bom_line_ids': [Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        self.component_product.write({'route_ids': [Command.link(self.dropship_route.id)]})

        self.assertIn(self.dropship_route.id, self.component_product.route_ids.ids,
                      "Dropship route should be assigned to the component")

        self.assertIn(self.dropship_subcontractor_route.id, self.component_product.route_ids.ids,
                      "Dropship subcontractor route should be automatically assigned to component used in subcontracting BOM when dropship is enabled")

        self.component_product.write({'route_ids': [Command.unlink(self.dropship_route.id)]})

        self.assertNotIn(self.dropship_subcontractor_route.id, self.component_product.route_ids.ids,
                         "Dropship subcontractor route should be automatically removed when dropship is disabled")

        bom.unlink()

    def test_06_bom_modification_route_update(self):
        """Test route updates when BOMs are modified"""

        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        self.assertIn(self.mfg_route.id, self.finished_product.route_ids.ids,
                      "Manufacture route should be assigned when normal BOM exists")

        bom.write({
            'type': 'subcontract',
            'subcontractor_ids': [Command.link(self.subcontractor.id)],
        })

        self.assertIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                      "Subcontract route should be assigned to component when BOM type changes to subcontract")

        self.component_product.write({'route_ids': [Command.link(self.dropship_route.id)]})

        self.assertIn(self.dropship_subcontractor_route.id, self.component_product.route_ids.ids,
                      "Dropship subcontractor route should be assigned when component has dropship and is used in subcontracting BOM")

        bom.write({'type': 'normal'})

        self.assertNotIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                         "Subcontract route should be removed when BOM type changes from subcontract")

        self.assertNotIn(self.dropship_subcontractor_route.id, self.component_product.route_ids.ids,
                         "Dropship subcontractor route should be removed when component is no longer used in subcontracting BOM")

        bom.unlink()

    def test_07_multiple_boms_route_handling(self):
        """Test route handling with multiple BOMs"""
        normal_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        another_product = self.env['product.template'].create({
            'name': 'Another Product',
            'type': 'consu',
            'categ_id': self.categ_all.id,
            'purchase_ok': True,
            'sale_ok': True,
        })

        subcontract_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': another_product.id,
            'product_qty': 1.0,
            'type': 'subcontract',
            'subcontractor_ids': [Command.link(self.subcontractor.id)],
            'bom_line_ids': [Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        self.assertIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                      "Subcontract route should be assigned to component used in subcontracting BOM")

        self.component_product.write({'route_ids': [Command.link(self.dropship_route.id)]})


        self.assertIn(self.dropship_subcontractor_route.id, self.component_product.route_ids.ids,
                      "Dropship subcontractor route should be assigned when component has dropship and is used in subcontracting BOM")


        subcontract_bom.unlink()

        self.assertNotIn(self.subcontract_route.id, self.component_product.route_ids.ids,
                         "Subcontract route should be removed when all subcontracting BOMs using the component are deleted")

        self.assertNotIn(self.dropship_subcontractor_route.id, self.component_product.route_ids.ids,
                         "Dropship subcontractor route should be removed when component is no longer used in any subcontracting BOM")

        normal_bom.unlink()


    def test_08_complex_bom_structure(self):
        """Test behavior with complex BOM structures"""
        intermediate_product = self.env['product.template'].create({
            'name': 'Intermediate Product',
            'type': 'consu',
            'categ_id': self.categ_all.id,
            'purchase_ok': True,
            'sale_ok': True,
        })

        intermediate_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': intermediate_product.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [Command.create({
                'product_id': self.component_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        finished_bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.id,
            'product_qty': 1.0,
            'type': 'subcontract',
            'subcontractor_ids': [Command.link(self.subcontractor.id)],
            'bom_line_ids': [Command.create({
                'product_id': intermediate_product.product_variant_id.id,
                'product_qty': 1.0,
            })],
        })

        self.assertIn(self.mfg_route.id, intermediate_product.route_ids.ids,
                      "Manufacture route should be assigned to intermediate product with normal BOM")

        self.assertIn(self.subcontract_route.id, intermediate_product.route_ids.ids,
                      "Subcontract route should be assigned to intermediate product used in subcontracting BOM")

        intermediate_product.write({'route_ids': [Command.link(self.dropship_route.id)]})

        self.assertIn(self.dropship_subcontractor_route.id, intermediate_product.route_ids.ids,
                      "Dropship subcontractor route should be assigned to intermediate product with dropship used in subcontracting BOM")

        finished_bom.unlink()

        self.assertNotIn(self.subcontract_route.id, intermediate_product.route_ids.ids,
                         "Subcontract route should be removed when subcontracting BOM is deleted")

        self.assertNotIn(self.dropship_subcontractor_route.id, intermediate_product.route_ids.ids,
                         "Dropship subcontractor route should be removed when subcontracting BOM is deleted")


        intermediate_bom.unlink()

        self.assertNotIn(self.mfg_route.id, intermediate_product.route_ids.ids,
                         "Manufacture route should be removed when normal BOM is deleted")

    def test_09_stock_rule_skip_invalid_configurations(self):
        """Test that stock rules are skipped for invalid configurations"""
        no_vendor_product = self.env['product.template'].create({
            'name': 'No Vendor Product',
            'type': 'consu',
            'categ_id': self.categ_all.id,
            'purchase_ok': True,
            'sale_ok': True,
        })

        no_vendor_product.write({'route_ids': [Command.link(self.buy_route.id)]})

        procurement_group = self.env['procurement.group'].create({
            'name': 'Test Procurement',
            'move_type': 'direct',
        })

        buy_rule = self.env['stock.rule'].search([
            ('route_id', '=', self.buy_route.id),
            ('action', '=', 'buy')
        ], limit=1)

        warehouse = self.env['stock.warehouse'].search([], limit=1)

        values = {
            'company_id': self.env.company.id,
            'date_planned': fields.Datetime.now(),
            'group_id': procurement_group.id,
            'warehouse_id': warehouse,
        }

        result = buy_rule._get_stock_move_values(
            no_vendor_product.product_variant_id,
            1.0,
            no_vendor_product.uom_id,
            warehouse.lot_stock_id,
            'Test Move',
            'Test Origin',
            self.env.company.id,
            values
        )

        self.assertFalse(result, "Buy rule should be skipped for product without vendors")

        no_bom_product = self.env['product.template'].create({
            'name': 'No BOM Product',
            'type': 'consu',
            'categ_id': self.categ_all.id,
            'purchase_ok': True,
            'sale_ok': True,
        })

        no_bom_product.write({'route_ids': [Command.link(self.mfg_route.id)]})

        manufacture_rule = self.env['stock.rule'].search([
            ('route_id', '=', self.mfg_route.id),
            ('action', '=', 'manufacture')
        ], limit=1)

        result = manufacture_rule._get_stock_move_values(
            no_bom_product.product_variant_id,
            1.0,
            no_bom_product.uom_id,
            warehouse.lot_stock_id,
            'Test Move',
            'Test Origin',
            self.env.company.id,
            values
        )

        self.assertFalse(result, "Manufacture rule should be skipped for product without BOM")
