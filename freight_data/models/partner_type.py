from odoo import fields, models


class PartnerType(models.Model):
    _name = 'partner.type'
    _description = 'Partner Type Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')