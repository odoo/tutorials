from odoo import models, fields


class InheritedModel(models.Model):
    _inherit = "res.users"
    property_ids=fields.One2Many("estate.property","salesperson_id",domain=[("state","!=","sold")], string="Properties")
