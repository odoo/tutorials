from odoo import fields, models, api

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(
        "Property Type", required = True,
        help = "This is a Many2One Field that defines the type of a property."
    )
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer("Sequence", help="Sequence of Property Type ordering.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")

    _sql_constraints = [('type_unique', 'unique(name)', 'Property Type should be unique.')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for line in self:
            line.offer_count = len(line.offer_ids)
