from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is Estate Property tage model like cozy, renovated"
    _order = "name"
    
    #---------------------------------------------------------------------
    # SQL Constraints
    #---------------------------------------------------------------------
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The property name tag should be unique')
    ]

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    name = fields.Char(string = "tag", required=True)
    color = fields.Integer()
