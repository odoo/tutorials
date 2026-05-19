from odoo import models, fields


class User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("est.property","user_id",string="Properties")