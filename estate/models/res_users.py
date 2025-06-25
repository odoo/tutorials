from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "Inheriting res.users"

    property_ids = fields.One2many(
        "estate.property",
        "sales_person",
        string="Properties",
        domain=[('date_availability', '>=', fields.Date.today())]
    )
