from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models, _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True, string="Property Type")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0.0)
            if property_id:
                property_record = self.env["estate.property"].browse(property_id)
                if property_record:
                    existing_prices = property_record.offer_ids.mapped("price")
                    if existing_prices and price < max(existing_prices):
                        raise exceptions.UserError(_("You cannot create an offer with a lower amount than an existing offer."))
        offers = super().create(vals_list)
        properties = offers.mapped("property_id").filtered(lambda p: p.state == "new")
        if properties:
            properties.write({"state": "offer_received"})
        return offers

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            elif record.date_deadline:
                delta = record.date_deadline - fields.Date.today()
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise exceptions.UserError(_("An offer has already been accepted for this property."))
            record.status = "accepted"
            other_offers = record.property_id.offer_ids.filtered(lambda o: o.id != record.id)
            other_offers.write({"status": "refused"})
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.buyer_id == record.partner_id and record.property_id.state == "offer_accepted":
                other_offers = record.property_id.offer_ids - record
                has_other_offers = other_offers.filtered(lambda o: o.status != "refused")
                record.property_id.write({
                    'selling_price': 0.0,
                    'buyer_id': False,
                    'state': 'offer_received' if has_other_offers else 'new'
                })
            record.status = "refused"
        return True
