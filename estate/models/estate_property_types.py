from odoo import fields, models

class EstatePropertyTypesModel(models.Model):
    _name="estate.property.types"
    _description = "The estate property types model"

    name = fields.Char(required=True)
    