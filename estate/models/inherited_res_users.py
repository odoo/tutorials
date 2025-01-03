from odoo import fields, models

class InheritedResUsers(models.Model):
    _inherit= "res.users"
    property_ids= fields.One2many(comodel_name="estate.property", inverse_name="salesperson", string="property_ids")