from odoo import fields, models


class EstateSalesperson(models.Model):
    _inherit = 'res.users'

    # relational fields
    property_ids = fields.One2many('estate.property', "salesperson_id", domain=[('state', 'in', ['new', 'offer_received'])])
