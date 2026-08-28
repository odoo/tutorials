from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
            'estate.property',
            'salesperson_id',
            string='Available properties')
