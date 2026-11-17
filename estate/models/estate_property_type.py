from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name desc"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_count_offer")

    _unique_tag_name = models.Constraint("UNIQUE(name)", "Tag name must be unique.")

    @api.depends("offer_ids")
    def _compute_count_offer(self):
        self.offer_count = len(self.offer_ids)
