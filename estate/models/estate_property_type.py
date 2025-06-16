from odoo import api,fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = 'sequence, name'

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    sequence = fields.Integer(string="Sequence", default=1, index=True, help="Used to order property types.")

    _sql_constraints = [('unique_property_type_name', 'UNIQUE(name)', 'A property type with this name already exists. Please choose a unique name.')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
