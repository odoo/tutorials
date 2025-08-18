from odoo import fields, models, api


class EstateProperties(models.Model):
    _name = "estate.property.types"
    _description = " Estate Property Types"
    _order = "sequence, name"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)',
         'The property type must be unique!!')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
