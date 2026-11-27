from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order properties. Lower is better."
    )

    # region computed fields
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offers Count")
    # endregion

    # region relationships
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )

    # region constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique"
    )
    # endregion

    # region private methods
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # endregion
