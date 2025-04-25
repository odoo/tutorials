from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [("check_property_tag_name", "unique(name)", "Two property tags cannot have the same name.")]
