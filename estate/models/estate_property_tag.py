from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"

    name = fields.Char(string="Property Tag", required=True)
    color = fields.Integer(string="Color")
    _unique_name = models.UniqueIndex("(name)", "A role with the same name already exists.")
