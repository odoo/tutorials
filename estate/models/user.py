from odoo import fields, models

class User(models.Model):
    pass # _inherit = ["res.users"]

    # property_ids = fields.One2many("estate.property", "salesperson_id")
