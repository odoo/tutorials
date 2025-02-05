from odoo import fields, models

class EstatePropertyTagsModel(models.Model):
    _name="estate.property.tags"
    _description = "The estate property tags model"

    name = fields.Char(required=True)
    