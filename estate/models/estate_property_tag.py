from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(string="Property Tag", required=True)
    _unique_name = models.UniqueIndex("(name)", "A role with the same name already exists.")
