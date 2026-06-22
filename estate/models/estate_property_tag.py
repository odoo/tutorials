from odoo import models,fields

class EstatePropertyTag(models.Model):
    _name ="estate.property.tag"
    _description = "Phis model provides tags for estate property"

    name= fields.Char(required=True)
    

