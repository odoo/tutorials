from odoo import models, fields


class InheritedUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",
        domain="[('status', 'in', ['new', 'offer_receive' , 'offer_accept'])]",
    )
