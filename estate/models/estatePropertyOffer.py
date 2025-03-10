from odoo import models, fields, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description =" Real Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    # set validity and date deadline dependent eachother and fill automatically
    @api.depends("create_date", "validity", "date_deadline")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()  # Fallback to today if not set
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                delta = (record.date_deadline - record.create_date.date()).days
                record.validity = delta

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
            for offer in record.property_id.offer_ids:
                if offer != record:
                    offer.status = "refused"
    
    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
    
    # constraints for offer 
    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "The offer price must be strictly positive.")
    ]
