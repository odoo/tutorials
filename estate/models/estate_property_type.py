from odoo import fields, models


class EstatePropertyType(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=1, help="Used to order property types")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")

    # ----------------------------------------
    # SQL constraints
    # ----------------------------------------
    _property_type_name_unique = models.Constraint("UNIQUE(name)")

    # ----------------------------------------
    # Compute methods
    # ----------------------------------------
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
