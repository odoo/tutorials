from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property',
        'salesperson_id',
        string="Properties",
        domain=[("state", "=", "new")]
    )