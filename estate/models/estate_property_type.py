from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate properties type"
    _order = "sequence, name"
    _sql_constraints = [
        ('type_name_unique', 'unique(name)', 'The type name must be unique.')
    ]

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many(
        comodel_name='estate.property', 
        inverse_name='property_type_id', readonly=True)
    sequence = fields.Integer('Sequence', 
        help="Used to order stages.")
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer', 
        inverse_name='property_type_id')
    offer_count = fields.Integer('Offer Count', 
        compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
