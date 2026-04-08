from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()

    _unique_tag_name = models.Constraint('UNIQUE (name)', "Tag name must be unique")
