from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name asc"

    _unique_tag = models.UniqueIndex("(name)", "Tag name must be unique in database")

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()
