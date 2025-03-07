from odoo import fields, models


class estatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Help to search Property by tags"

    name = fields.Char(string="Tag", required=True)

    _sql_constraints = [("unique_tag_name", "UNIQUE(name)", "Tag name must be unique.")]
