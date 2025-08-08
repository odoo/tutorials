from odoo import fields, models


class estatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Help to search Property by tags"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [("unique_tag_name", "UNIQUE(name)", "Tag name must be unique.")]
