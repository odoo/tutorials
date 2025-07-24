from odoo import models, fields, api

class EstatePropertyType(models.Model):

    _name ="estate.property.type"
    _description = "Property type"

    _order="sequence,name"

    _sql_constraints = [
        ('unique_name','UNIQUE(name)',
        'Type names should be unique')
    ]

    sequence = fields.Integer('Sequence',default=1)

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property","property_type_id")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")


    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            for line in record.offer_ids:
                record.offer_count+=1
    