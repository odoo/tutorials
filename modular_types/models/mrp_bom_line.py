from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    modular_type_id = fields.Many2one(
        'product.modular.type',
        string='Modular Type',
        domain="[('id', 'in', allowed_modular_type_ids)]",
    )

    allowed_modular_type_ids = fields.Many2many(
        'product.modular.type', compute='_compute_allowed_modular_type_ids', store=False
    )

    @api.depends('bom_id.product_tmpl_id')
    def _compute_allowed_modular_type_ids(self):
        for line in self:
            if line.bom_id.product_tmpl_id:
                line.allowed_modular_type_ids = (
                    line.bom_id.product_tmpl_id.modular_type_ids
                )
            else:
                line.allowed_modular_type_ids = self.env[
                    'product.modular.type'
                ].search([])
