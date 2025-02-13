from odoo import fields, models,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property"
    _order = "sequence,name"

    sequence = fields.Integer('Sequence', default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)', 
         'A property type must be unique.')
    ]
       