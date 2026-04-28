from odoo import exceptions, api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _check_price = models.Constraint(
    'CHECK(price > 0)',
    'An offer price must be strictly positive',
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(start_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = fields.Date.to_date(offer.create_date) or fields.Date.today()
            offer.validity = (offer.date_deadline - start_date).days

    def accept_offer(self):
        for offer in self:
            if offer.property_id.garden and offer.property_id.garden_orientation == 'south' and offer.price < offer.property_id.expected_price:
                raise exceptions.ValidationError("The offer price must be higher than the expected price for this property.")
            else:
                offer.status = 'accepted'
                offer.property_id.selling_price = offer.price
                offer.property_id.buyer_id = offer.partner_id
                offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
            offer.property_id.selling_price = offer.price
        return True
