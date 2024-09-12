from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "EstatePropertyTag"
    _order = "name"

    name = fields.Char(string="tag", required=True)
    _sql_constraints = [
        ("uniq_propertytag", "unique(name)", "A property tag name must be unique"),
    ]
    color = fields.Integer("color index")
