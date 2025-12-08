from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_modular_type = fields.Boolean(
        string='Has Modular Type',
        compute='_compute_has_modular_type',
        help="Technical field to check if the product's BoM has modular components."
    )
    source_modular_type_id = fields.Many2one(
        'modular.type.config',
        string="Source Modular Type",
        readonly=True,
        copy=False
    )

    @api.depends('product_id')
    def _compute_has_modular_type(self):
        if not self.product_id:
            self.has_modular_type = False
            return

        boms = self.env['mrp.bom']._bom_find(
            self.product_id,
            company_id=self.company_id.id,
            bom_type='normal'
        )
        for line in self:
            line.has_modular_type = False
            bom = boms.get(line.product_id)
            if bom:
                if any(bom_line.modular_type_id for bom_line in bom.bom_line_ids):
                    line.has_modular_type = True

    def action_configure_modular_line(self):
        self.ensure_one()

        boms_dict = self.env['mrp.bom']._bom_find(
            self.product_id,
            company_id=self.company_id.id,
            bom_type='normal'
        )
        bom = boms_dict.get(self.product_id)

        if not bom:
            return True

        wizard_lines_vals = []
        for bom_line in bom.bom_line_ids:
            if bom_line.modular_type_id:
                wizard_lines_vals.append((0, 0, {
                    'modular_type_id': bom_line.modular_type_id.id,
                    'component_product_id': bom_line.product_id.id,
                    'default_quantity': bom_line.product_qty * self.product_uom_qty,
                    'new_quantity': bom_line.product_qty * self.product_uom_qty,
                }))

        if not wizard_lines_vals:
            return True

        wizard = self.env['modular.line.generator.wizard'].create({
            'sale_order_id': self.order_id.id,
            'wizard_line_ids': wizard_lines_vals,
        })

        return {
            'name': 'Set Modular Type Values',
            'type': 'ir.actions.act_window',
            'res_model': 'modular.line.generator.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }
