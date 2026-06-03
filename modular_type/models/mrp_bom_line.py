from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    modular_type_id = fields.Many2one(
        "modular.type",
        string="Modular Type",
    )
