from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'sales_person_id', domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')])
    