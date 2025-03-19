from odoo import api,fields, models
from datetime import date, timedelta

class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "reals estate properties"

    name = fields.Char('Property Type Name',required=True)
    property_type_id= fields.Char('Property Type ID',required=True)
    properties = fields.One2many("estate.property","property_type_id",string="properties")
    offer_ids=fields.One2many("estate.property.offer","offer_type_id",string="offers")
    offer_count=fields.Integer(compute="_compute_offer_count",default=0)
    _order ="sequence"
    sequence=fields.Integer('Sequence',default=1,help="Used to order porperties")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'There is already a type with this name'),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self: 
            record.offer_count=len(record.offer_ids)
