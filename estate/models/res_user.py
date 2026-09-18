from odoo import models, fields


class ResUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property',
                                   'salesman_id',
                                   'Salesperson',
                                   domain = lambda self: [('state', 'in', ('new', 'offer_received'))])