from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Real Estate Property Tag Model"

    name=fields.Char(required=True)

    _sql_constraints=[('tag_name_unique','UNIQUE(name)','Tag name must be unique')]
