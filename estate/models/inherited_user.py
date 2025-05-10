from odoo import models, fields


class InheritedUser(models.Model):
    # _inherit is used to extend the existing model 'res.users'
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "salesperson_id", string="Estate Properties"
    )
