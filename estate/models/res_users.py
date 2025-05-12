from odoo import fields, models


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property', 
        'salesperson_id',  # Ensure this is the correct inverse field in `estate.property`
        string='Managed Properties',
        domain=[('state', 'in', ['new', 'offer_received'])]
    )
    