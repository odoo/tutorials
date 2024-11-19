from odoo import fields, models, api


class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'estate_property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    _sql_constraints = [
        ('check_unique_name', 'unique(name)',
         'Type name must be unique.'),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = 0
            if record.offer_ids:
                record.offer_count = len(record.offer_ids)
