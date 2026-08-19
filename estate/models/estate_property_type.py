from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "name"

    name = fields.Char("Type Name", required=True)
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )

    # One2many relations
    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )

    # Computed
    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # Constraints
    _unique_name = models.Constraint("UNIQUE(name)", "Property Type name must unique!")
