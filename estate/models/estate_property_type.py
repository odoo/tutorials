from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order = 'sequence ASC, name ASC'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types")    
    property_ids  = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_count_num_offers")

    @api.depends("offer_ids")
    def _count_num_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]
