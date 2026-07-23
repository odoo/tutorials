from odoo import api, fields, models


class PropertyType(models.Model):
    # Attributes
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    # Fields
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)

    # Relational Fields
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    # Computed Fields
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    # SQL Constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    # Compute Methods
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
