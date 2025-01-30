from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'  # Extending res.users

    property_ids = fields.One2many(
        'estate_property',  # Related model
        'seller_id',   # Inverse field (must exist in estate.property)
        string="Properties",
        domain=[('state', '=', 'new')]  # Only list available properties
    )
