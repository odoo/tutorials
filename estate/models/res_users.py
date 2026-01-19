from odoo import fields, models

class ResUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson",
        string="Properties",
        domain="[('state', '!=', 'sold')]"
    )

    sales_fee = fields.Float(
        string="Salesperson Fee",
        default=1000
    )
