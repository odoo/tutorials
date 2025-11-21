from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price"

    price = fields.Float("Price", required=True)
    state = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        default=False,
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", store=True
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer._origin.validity:
                offer.date_deadline = fields.Date.add(
                    offer.create_date.date(), days=offer.validity
                )
            else:
                offer.date_deadline = False

    def action_accept(self):
        for offer in self:
            offer.state = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id.id
            offer.property_id.state = 'offer_accepted'
            other_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.id != offer.id and o.state != 'refused'
            )
            other_offers.state = 'refused'
        return True

    def action_refuse(self):
        for offer in self:
            offer.state = 'refused'
        return True
