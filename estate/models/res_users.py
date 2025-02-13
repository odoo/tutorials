from odoo import fields, models, views, api

class ResUsers(models.MOdel):
    _inherit = "res.users"

#-------------------------------------Relational Fields--------------------------------------#
    property_ids = fields.One2many(comodel="estate.property", inverse_name="seller_id", domain=[('state', 'in', ['new', 'offer_received'])]
    )

