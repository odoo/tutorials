from odoo import models,fields

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    property_ids = fields.One2many("estate.property", "salesman_id", string="Properties", domain=[("state", "in", ["new", "offer_received"])])
