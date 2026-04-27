from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(string="name", required=True)
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Property Type",
    )
    offer_ids = fields.One2many('estate.property.offer', inverse_name='property_type_id')
    offer_count = fields.Integer(string="Total Offer", compute='_compute_offer_count')
    sequence = fields.Integer("Sequence", default=1)

    _name_check = models.Constraint("UNIQUE (name)", "Please add unique type")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
    
        
