from odoo import fields, models

class EstatePropertyExtendUsers(models.Model):
    _inherit = "res.users"


    property_ids = fields.One2many("estate.property", 'salesperson_id', string="User Properties",
                                   domain=[('state', 'in', ['new', 'offer_received'])])
