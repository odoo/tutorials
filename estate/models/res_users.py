from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(string="Property Ids", comodel_name='estate.property', inverse_name='sales_id')
