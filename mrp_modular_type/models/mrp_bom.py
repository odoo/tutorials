from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    modular_type_id = fields.Many2one(
        comodel_name='modular.type',
        string="Modular Type",
        domain="[('id', 'in', available_modular_type_ids)]"
    )

    available_modular_type_ids = fields.Many2many(
        comodel_name='modular.type',
        compute='_compute_available_modular_types',
        string="Available Modular Types",
        store=False
    )

    @api.depends('product_id')
    def _compute_available_modular_types(self):
        for line in self:
            line.available_modular_type_ids = line.parent_product_tmpl_id.modular_type_ids if line.product_id else False
