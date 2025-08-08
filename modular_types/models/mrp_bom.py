from odoo import fields, models, api


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    modular_type_id = fields.Many2one('modular.type', domain="[('id', 'in', available_modular_type_ids)]")

    available_modular_type_ids = fields.Many2many(
        'modular.type',
        compute='_compute_available_modular_types',
        string="Available Modular Types",
    )

    @api.depends('product_id')
    def _compute_available_modular_types(self):
        for line in self:
            line.available_modular_type_ids = line.parent_product_tmpl_id.modular_types if line.product_id else False
