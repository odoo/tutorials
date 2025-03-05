from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    modular_type_id = fields.Many2one(
        comodel_name="mrp.modular.type",
        string="Modular Type",
    )
