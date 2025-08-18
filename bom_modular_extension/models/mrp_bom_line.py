from odoo import fields, models, api


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    modular_type_id = fields.Many2one(
        "modular.type",
        string="Modular Type",
        domain="[('id', 'in', filter_modular_type_ids)]",
        help="Specify which modular type this BOM line belongs to",
    )

    filter_modular_type_ids = fields.Many2many(
        "modular.type",
        compute="_compute_available_modular_types",
        string="Available Modular Types",
    )

    @api.depends("bom_id.product_tmpl_id")
    def _compute_available_modular_types(self):
        for line in self:
            product_tmpl = line.bom_id.product_tmpl_id
            line.filter_modular_type_ids = (
                product_tmpl.modular_type_ids if product_tmpl else False
            )
