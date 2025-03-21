from odoo import models, fields

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "sale_id", string="Properties",
                                   domain=['|', ('state', '=', 'new'), ('state', '=', 'offer received')])
