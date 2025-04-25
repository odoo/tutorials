from odoo import fields, models


class EstateTagsModel(models.Model):
    _name = 'estate.property.tags'
    _description = 'Estate property tags'

    name = fields.Char('Title', required=True, translate=True)
