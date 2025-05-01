from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        (
            "check_name",
            "UNIQUE(name)",
            "The name must be unique",
        )
    ]
    _order = "sequence,name"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order types")
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        string="Number of Offers",
        compute="_compute_offer_count",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
