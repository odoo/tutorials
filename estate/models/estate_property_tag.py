from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_name = models.UniqueIndex("(name)", "All property tags need to have a unique name")
