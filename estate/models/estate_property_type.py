from odoo import models, fields, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    # constraints
    _unique_type = models.Constraint(
        'UNIQUE(name)',
        'Type name should be unique',
    )

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", inverse_name="property_type_id", string="Properties")
    sequence = fields.Integer(string="Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.offer_ids)
