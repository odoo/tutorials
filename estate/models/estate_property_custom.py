from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"
    _description = "Inheriting res.users"

    property_ids = fields.One2many(
        "estate.property",
        "sales_person",
        string="Properties",
        domain="[('date_availability', '>=', context_today())]" 
    )
