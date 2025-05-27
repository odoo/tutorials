from odoo import models, fields


class EstateCustomUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", inverse_name='salesperson_id', string="Available Properties",
                                   domain=[('state', 'in', ['new', 'offer_received'])])
