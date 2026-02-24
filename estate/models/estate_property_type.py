from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    _rec_name = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.'
    )
    property_ids = fields.One2many(
        'estate.property',
        'property_type_id',
        string="Properties"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count",
        store=True
    )

    @api.depends('name', 'sequence', 'offer_count')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.sequence}] {record.name} ({record.offer_count} Offers)"

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
