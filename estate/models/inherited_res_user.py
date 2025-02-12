from odoo import fields, models


class Inherited_res_user(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesman_id", string="Properties (Salesperson)", domain="[('salesman_id.state', 'in', ['new', 'cancelled'])]")
