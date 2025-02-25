from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many('estate.property', 'salesman', domain=['&', ('date_availability', '>=', fields.Date.today()), '|', ('state', '=', 'new'), ('state', '=', 'offer_received')])
    