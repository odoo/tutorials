from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.tags"
    _description = "Tags for Estate"
    _oreder="name"

    name = fields.Char("Tag", required=True)

    _sql_constraints = [("unique_tag_name", "unique(name)", "Tag already exists.")]
