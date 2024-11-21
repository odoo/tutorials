from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='user_id')
