from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    property_ids = fields.One2many(
        string="Properties",
        comodel_name="estate.property",
        inverse_name="property_type_id",
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
    )
    offer_count = fields.Integer(
        string="Number of Offers",
        compute="_compute_offer_count",
    )

    # Methods
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
