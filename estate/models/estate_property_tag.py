from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    name = fields.Char("Name", required=True)
    _name_unique = models.Constraint("unique(name)", "Tag name must be unique")
