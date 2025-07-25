from odoo import fields, models


class ResUsers(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = 'res.users'
    _inherit = 'res.users'

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    property_ids = fields.One2many(
        'estate.property',
        'salesperson_id',
        string="Properties",
        domain="[('state', 'in', ['new', 'offer_received'])]",
    )
