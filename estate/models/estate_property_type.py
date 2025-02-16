from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type Model"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property","property_type_id")
    offer_ids = fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count',string="Offer Count")
    sequence = fields.Integer('Sequence')

    _sql_constraints = [('type_name_unique','UNIQUE(name)','Type name must be unique')]

    # Computation methods
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ids)
