from odoo import fields, models
from datetime import date, timedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "reals estate properties"

    name = fields.Char('Property Type Name',required=True)
    property_type_id= fields.Char('Property Type ID',required=True)
    properties = fields.One2many("estate.property","property_type_id",string="properties")
    _order ="sequence"
    sequence=fields.Integer('Sequence',default=1,help="Used to order porperties")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'There is already a type with this name'),
    ]
