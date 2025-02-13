from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='salesperson', string='Properties', domain="[('state', 'in', ['new', 'offer_received'])]")
