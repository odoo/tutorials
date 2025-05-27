from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="sales_person",
        domain="""[
            ('state', 'in', ('new', 'offer_received'))
        ]"""
    )