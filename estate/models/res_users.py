from odoo import fields, models

class res_users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property","sales_person_ids", string=" ", domain=[('status', 'in', ['new', 'offer_received'])])
