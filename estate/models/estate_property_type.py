from odoo import api, models, fields


class PropertyType(models.Model):

    # -------------------------------------------------------------------------
    # Private attributes
    # -------------------------------------------------------------------------
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    # -------------------------------------------------------------------------
    # Field declarations
    # -------------------------------------------------------------------------
    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1)

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    # -------------------------------------------------------------------------
    # SQL constraints
    # -------------------------------------------------------------------------
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        "The property type name must be unique."
    )

    # -------------------------------------------------------------------------
    # Compute methods
    # -------------------------------------------------------------------------
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
