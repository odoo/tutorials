from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    property_ids = fields.One2many(string="Properties", comodel_name="estate.property", inverse_name="property_type_id")
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Number Of Offers", compute="_compute_number_of_offers")
    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used for manual ordering!")
    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'The property type name must be unique!')]

    @api.depends("offer_ids")
    def _compute_number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
