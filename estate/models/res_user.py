from odoo import fields, models


class ResUsers(models.Model):
    _inherit = ["res.users"]
    _name = "res.users"

    property_ids = fields.One2many('estate.property',
                                   'user_id',
                                   domain=[("state", "not in", ["sold", "cancelled"])])
