from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _order = 'name asc'

    estate_property_ids = fields.Many2many(comodel_name="estate.property")
    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color", default=0)

    _check_unique_name = models.UniqueIndex(definition="(UPPER(name))", message="Tag should be unique")
