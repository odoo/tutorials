from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class ResUsers(models.Model):
    _inherit = 'res.users'
    _name = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id',
                                   domain=['|', ('state', '=', 'new'), ('state', '=', 'offer received')])
