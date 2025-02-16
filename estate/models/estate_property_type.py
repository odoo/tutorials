from odoo import models, fields, api


class EstatePropertyType(models.Model):

    # ..................private attributes..................
    _name = "estate.property.type"
    _description = "These are Estate Module Property Types"
    _order = "name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property type name must be unique"),
    ]

    # ..................field attributes..................
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    # ..................relational attributes..................
    property_ids = fields.One2many(string="Properties", comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_type_id")

    # ..................compute methods..................
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
