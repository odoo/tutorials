from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Phis model provides tags for estate property"

    name = fields.Char(required=True)
    # property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    # type_ids=fields.one2many('estate.property.type','',)
