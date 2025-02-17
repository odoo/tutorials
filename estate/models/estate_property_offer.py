from odoo import api, exceptions, fields, models
from datetime import timedelta


class EstatePropertyOffers(models.Model):
    _name = 'estate.property.offers'
    _description = 'Real estate property offers'
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offered price must be greater then 0.'),
    ]

    price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity_days = fields.Integer(string="Valid till")
    deadline = fields.Date(compute='_compute_deadline', store=True, inverse="_inverse_deadline")
    offer_state = fields.Selection(
        string="Offer State",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ], 
        copy=False
    )

    # Computes deadline using validity days
    @api.depends("validity_days")
    def _compute_deadline(self):
        for record in self:
            if record.validity_days:
                record.deadline = fields.Date.today() + timedelta(days=record.validity_days)

    # Let's user select manually as well.
    @api.depends("validity_days")
    def _inverse_deadline(self):
        for record in self:
            if record.validity_days:
                record.deadline = fields.Date.today() - timedelta(days=record.validity_days)

    # Sets offer state to accepted when called
    def action_offer_confirm(self):
        for record in self:
            if record.property_id.offers_id.filtered(lambda offer: offer.offer_state == 'accepted'):
                raise exceptions.UserError("You can't accept two offers!")
            record.offer_state = 'accepted'
            record.property_id.state = 'offer accepted'
            record.property_id.selling_price = record.price
    
    # Sets offer state to refused when called
    def action_offer_cancel(self):
        for record in self:
            record.offer_state = 'refused'

    @api.model
    def create(self, vals_list):
        record = super().create(vals_list)
        for offer in self:
            if offer.property_id:
                offer.property_id.state = 'offer received'        
        return record
