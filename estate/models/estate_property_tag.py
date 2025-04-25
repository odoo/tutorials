from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate: Tag"
    _order = "name asc"

    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [("tag_name_unique", "UNIQUE(name)", "A tag with the same name already exists.")]
