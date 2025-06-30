from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many( 
        comodel_name="estate.property",
        inverse_name="salesperson",
        domain=[("state", "not in", ["canceled", "sold"])],
    )