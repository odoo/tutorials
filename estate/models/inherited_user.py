from odoo import models, fields


class InheritedResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', inverse_name='salesman_id',
                                   domain=[('state', 'in', ['new', 'offer_received'])])
