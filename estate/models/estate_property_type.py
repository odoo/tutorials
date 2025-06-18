from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Store Real Estate Properties Types"

    name = fields.Char("Estate Type Name", required=True, translate=True)

