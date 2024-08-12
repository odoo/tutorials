from odoo import models, fields, api


class EstatePropertytype(models.Model):

    _name = "estate.property.type"
    _description = "estate property type description"
    _order = "sequence"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         "A property type with the same name already exists")
    ]
    property_ids = fields.One2many('estate.property', "property_type_id")
    sequence = fields.Integer('Sequence')

    offer_ids = fields.One2many(
        "estate.property.offer", string="Offer", inverse_name='property_type_id')
    offer_count = fields.Integer(
        string="Offer Count",
        compute='_compute_offer_count'
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
