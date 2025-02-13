from odoo import api, fields, models 


class Estate_Property_Type (models.Model):
    _name = "estate_property_type_model"
    _description = "This is a property type model"
    _sql_constraints = [
        ("check_type_name", "UNIQUE(name)", "type name should be unique")
    ]

    _order = "sequence, name"
    sequence = fields.Integer('Sequence', default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate_model", "property_type_id")
    offer_ids = fields.One2many("estate_property_offer_model", 'property_type_id', string="Offers")
    offer_count = fields.Integer(string='Offer Count', default=0, compute='_compute_offer_count', store=True)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    
    