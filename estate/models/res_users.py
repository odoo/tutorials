
from odoo import fields, models, api

class ResUsers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="salesperson_id", domain="['|',('state','=','new'),('state','=','offer received')]")