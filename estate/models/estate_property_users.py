from odoo import fields, models


class EstatePropertyUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesman",
                                   domain=[('state', 'in', ('new','offer received'))])
