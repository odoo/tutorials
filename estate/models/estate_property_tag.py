from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of property"
    _check_unique = models.UniqueIndex("(name)", "All property tags need to have a unique name")

    name = fields.Char(required=True)
