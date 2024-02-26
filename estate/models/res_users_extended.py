from odoo import models, fields

class UsersExtended(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.property", "salesman_id")

