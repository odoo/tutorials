from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(string="Tag", required=True)

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'Property Tag Must be Unique')]
