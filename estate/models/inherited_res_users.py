from odoo import fields, models

class InheritedResUser(models.Model):
    # _name = "inherited.res.users"
    # _description = "inherited class of res users"
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", domain=[('state', 'in', ('new', 'offer_received'))])

