from odoo import Command, fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    applied_modular_types = fields.Many2many(
        'product.modular.type', compute='_compute_applied_modular_types', readonly=True
    )

    def _compute_applied_modular_types(self):
        for bom in self:
            modular_types = bom.bom_line_ids.mapped('modular_type_id')
            bom.applied_modular_types = [Command.set(modular_types.ids)]
