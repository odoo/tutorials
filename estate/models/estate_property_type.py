from odoo import api,fields, models


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type Model"
    _order = "sequence,name asc"

    name = fields.Char(required = True)
    property_ids = fields.One2many("estate.property","property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids=fields.One2many("estate.property.offer","property_type_id")
    offer_count=fields.Integer(compute='_compute_offer_count',string="Offer Count")

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count=len(record.offer_ids)
