from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    modular_type_id = fields.Many2one(
        "module.types",
        domain="[('id', 'in', available_modular_type_ids)]",
        string="Module Types",
    )

    available_modular_type_ids = fields.Many2many(
        "module.types", compute="_compute_available_modular_ids"
    )

    @api.depends("product_id", "parent_product_tmpl_id")
    def _compute_available_modular_ids(self):
        for line in self:
            line.available_modular_type_ids = (
                line.parent_product_tmpl_id.modular_types if line.product_id else False
            )

