from odoo import fields, models


class ResUsers(models.Model):
    _inherit = ['res.users']

    # this seems to not filter the same properties out as the one in estate_property_views, even though I copied the domain?
    property_ids = fields.One2many('estate.property', 'salesperson_id', domain=[('date_availability', '<=', 'today')])
