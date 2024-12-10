from odoo import models, fields, api

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)