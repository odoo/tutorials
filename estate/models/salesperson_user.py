from odoo import models, fields


class SalespersonUser(models.Model):
    _inherit = "res.users"
    _description = "User extended with the properties related to the salesperson properties"

    # One2many relationships
    property_ids = fields.One2many("estate.property", "salesperson_id", domain="[('state', 'in', ['new', 'offer received'])]")
