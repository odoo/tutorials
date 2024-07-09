from odoo import fields, models


class propertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the Real Estate Property"

    name = fields.Char("Tags", required=True)

    _sql_constraints = [('name_uniq', "unique(name)", "Name of Property Tag must be Unique")]
