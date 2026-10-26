from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties type declaration"
    _order = "sequence, name asc"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=1, help="Used to order type. Lower is better.")
    offer_ids = fields.One2many(related="property_ids.offer_ids")

    # -------------------------------------------------------------
    # Constraints
    # -------------------------------------------------------------
    _unique_name = models.Constraint(
        'unique(name)',
        'A property type name must be unique.',
    )

    # -------------------------------------------------------------
    # Computed fields and their method
    # -------------------------------------------------------------
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
