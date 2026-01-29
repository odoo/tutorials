from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta
import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    _check_price = models.Constraint('CHECK(price > 0)', 'The price should always be positive')

    price = fields.Float()
    status = fields.Selection(readonly=True, selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_validity", readonly=False)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.model
    def create(self, vals_list):
        if(len(vals_list) == 0):
            return super().create(vals_list)

        prop = self.env['estate.property'].browse(vals_list[0]['property_id'])

        if (prop.state != 'new' and prop.state != 'offer-received'):
            raise exceptions.UserError("Cannot add an offer to a property not accepting offers")

        if (any(o.price > vals_list[0]['price'] for o in prop.offer_ids)):
            raise exceptions.UserError("Cannot add an offer with a lower amount than an existing one")

        prop.state = "offer-received"

        return super().create(vals_list)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            create = offer.create_date.date() if isinstance(offer.create_date, datetime.datetime) else fields.Date.today()
            offer.date_deadline = create + relativedelta(days=offer.validity)

    def _inverse_validity(self):
        for offer in self:
            create = offer.create_date.date() if isinstance(offer.create_date, datetime.datetime) else fields.Date.today()
            offer.validity = (offer.date_deadline - create).days

    def accept_offer(self):
        for offer in self:
            if (offer.status == 'accepted'):
                continue

            for other in offer.property_id.offer_ids:
                if (other.status == 'accepted'):
                    raise exceptions.UserError("Cannot accept multiple offers for a single property")

            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer-accepted"
        return True

    def refuse_offer(self):
        for offer in self:
            if (offer.status == 'accepted'):
                offer.property_id.buyer_id = None
                offer.property_id.selling_price = None
            offer.status = 'refused'
        return True
