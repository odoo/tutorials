

# This model inherits from res.users model 

from odoo import models, fields

class InheritedResUsers(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many('estate.property', 'user_id', "Estate Property",
        domain=[('state', 'in', ['new','offer_received'])]
    )

