from odoo import api, fields, models
from datetime import timedelta
from odoo import exceptions
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        copy = False,
        selection=[
            ("accepted", "Accepted"),
            ("refused","Refused")
        ])
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required = True)
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            accepted_offer = self.search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ], limit=1)
            if accepted_offer:
                raise UserError("Only one offer can be accepted per property!")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.status = "offer accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.status = "new"

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]
