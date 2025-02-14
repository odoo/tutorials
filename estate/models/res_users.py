from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"  # Extend res.users model

    property_ids = fields.One2many(
        "estate.property",  # Related model
        "user_id",  # Field in estate.property linking to res.users
        string="Properties"
    )
