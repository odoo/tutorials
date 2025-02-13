from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is Estate Property tage model like cozy, renovated"

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    name = fields.Char(string = "tag", required=True)
