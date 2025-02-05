from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "These are the tags for estate properties"

    name = fields.Char(required=True)

    _sql_constraints = [("uniq_tag", "unique(name)", "Tags should have a unique name")]
