from odoo import fields, models, api

class estate_property_type(models.Model):
    _name = "estate.property.type"  
    _description = "real estate property types"
    _order = "sequence, name"

    property_type = fields.Text()
    name = fields.Char()
    sequence = fields.Integer(string='Sequence', default=1)

    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id") 
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(string="Offer Count",
        compute="_compute_offer_count",
        store=True)   

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)