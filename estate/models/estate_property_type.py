from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "name asc"

    name = fields.Char(string="Title", required=True, translate=True)
    property_ids = fields.One2many(
        "estate.property", inverse_name="property_type_id", string="Property"
    )
    offer_ids = fields.Many2many(related="property_ids.offer_ids")
    offer_count = fields.Integer(
        string="Number of offers", compute="_compute_offer_count"
    )
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(
        string="Sequence", default=1, help="Used to order types. Lower is better."
    )

    _sql_constraints = [
        (
            "check_unique_name",
            "UNIQUE(name)",
            "Tag already exists.",
        ),
    ]

    @api.depends("offer_count")
    def _compute_offer_count(self):
        """
        The function calculates the number of offers by counting the elements in the list of offer IDs.
        """
        self.offer_count = len(self.offer_ids)
