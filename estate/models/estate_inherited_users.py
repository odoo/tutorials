from odoo import fields, models


class EstateInheritedUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='salesperson',
        string='Estate Properties',
        domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')],
    )
