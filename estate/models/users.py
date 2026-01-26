from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id', domains = "[('state', 'in', ('new', 'offer_received'))]")
