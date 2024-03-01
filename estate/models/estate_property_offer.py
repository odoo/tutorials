from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property"
    _offer = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('refused', 'Refused'),
            ('accepted', 'Accepted')
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK (price > 0)', 'Offer price must be strictly positive.')
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def estate_offer_accept(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            for property_offer in offer.property_id.offer_ids:
                if (property_offer.id != offer.id):
                    property_offer.status = "refused"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def estate_offer_refuse(self):
        for offer in self:
            offer.status = "refused"
            if offer.property_id.buyer_id == offer.partner_id:
                offer.property_id.buyer_id = None
                offer.property_id.selling_price = 0
                offer.property_id.state = "offer_received"
        return True

    @api.model
    def create(self, vals):
        property = self.env["estate.property"].browse(vals["property_id"])
        if property.state == "sold":
            raise UserError("You cannot create an offer for a sold property")
        if vals["price"] < property.best_price:
            raise UserError("You can't create an offer with a lower price than the Best Offer.")
        property.state = "offer_received"
        return super().create(vals)
