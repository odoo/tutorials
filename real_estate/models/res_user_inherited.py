from odoo import models, fields # type: ignore

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.properties", "users_id", string="Salesperson")
