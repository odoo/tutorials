from odoo import models,fields

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type Model"

    name=fields.Char(required=True)

    _sql_constraints=[('type_name_unique','UNIQUE(name)','Type name must be unique')]
