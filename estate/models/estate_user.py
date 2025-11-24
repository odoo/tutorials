from odoo import models, fields


class EstateUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property', 'sales_person_id',
        string='Real Estate Properties',
        domain=[('state', 'in', ('new', 'cancelled', 'offer_received'))]
    )
