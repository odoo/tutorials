from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property"
    _offer = "price desc"

    price = fields.Float()
    status = fields.Selection([
        ('refused', 'Refused'),
        ('accepted', 'Accepted')
    ], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if (offer.create_date):
                offer.date_deadline = fields.Datetime.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if (offer.create_date):
                offer.validity = (offer.date_deadline - offer.create_date).days
            else:
                offer.validity = (offer.date_deadline - fields.Datetime.today()).days

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
            if (offer.property_id.buyer_id == offer.partner_id):
                offer.property_id.buyer_id = None
                offer.property_id.selling_price = 0
                offer.property_id.state = "offer_received"
        return True
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK (price > 0)', 'Offer price must be strictly positive.')
    ]
