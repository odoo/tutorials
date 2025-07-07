

# the tag model will be here



from odoo import fields, models



class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag model for the estate properties"
    name = fields.Char(required=True)
