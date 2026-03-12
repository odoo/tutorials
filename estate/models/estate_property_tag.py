from odoo import fields, models


class EstatePropertytTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate_property_tag'
    _unique_tag = models.UniqueIndex('(name)','The name of the tag must be unique')
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()
