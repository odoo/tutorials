from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="seller_id", string="Properties", domain=[('state', 'in', ['new', 'offerreceived'])])
