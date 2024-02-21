from odoo import models, fields


class EstateUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", string="Properties", domain=[('state', 'in', ('new', 'offer_received'))])
