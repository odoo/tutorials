from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "EstatePropertyTag"
    _order = "name"

    _sql_constraints = [
        ("uniq_propertytag", "unique(name)", "A property tag name must be unique")
    ]
    name = fields.Char(string="tag", required=True)
    color = fields.Integer("color index")
