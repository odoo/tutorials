from odoo import fields,models

class ResUsers(models.Model):
    _inherit = 'res.users'
    _description = 'Users of estate module'

    property_ids= fields.One2many('estate.property','user_id', string="Real Estate Properties")
