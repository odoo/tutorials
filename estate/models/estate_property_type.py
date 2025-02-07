from odoo import fields, models

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type Model"

    name = fields.Char(required=True)
    property_ids= fields.One2many('estate.property','property_type_id',string="Properties")
