from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name desc"
    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type must be unique'),
    ]

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id", string="Offer Id")
    offer_count = fields.Integer(string="Total Offers", compute="_compute_total_offers")

    # === COMPUTE METHODS === #
    @api.depends('offer_ids')
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
