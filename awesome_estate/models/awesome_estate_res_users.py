from odoo import _, fields, models


class AwesomeEstateResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'awesome.estate.property',
        'salesperson_id',
        string="Estate Properties",
        domain=[('state', 'in', ('new', 'offer_received', 'offer_accepted'))],
    )
