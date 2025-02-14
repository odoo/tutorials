from odoo import fields, models

class InheritedUsers(models.Model):
    _inherit = 'res.users'

# ------------------------------Relational Fields--------------------------------------#
    property_ids = fields.One2many('estate.property', inverse_name='seller_id')
