from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Tags for properties"

    name = fields.Char(required=True)
