from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is the model for the estate property type"
    _order = "name"


    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id", string="Property")
    sequence = fields.Integer(string="Sequence", default=1, help="Used to order types")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_property_type", "UNIQUE(name)", "The same property type is already exist")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
