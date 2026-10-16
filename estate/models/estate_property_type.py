from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char("Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("Offer count", compute="_compute_offer_count")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name of a property type should be unique.',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        self.offer_count = len(self.offer_ids)
