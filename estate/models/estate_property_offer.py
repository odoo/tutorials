from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ESTATE property tag"
    _order = "price desc"

    currency_id = fields.Many2one(
        "res.currency",
        related="property_id.currency_id")
    price = fields.Monetary(currency_field='currency_id')
    state = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False, readonly=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, compute="_compute_validity", inverse="_inverse_validity")
    date_deadline = fields.Date()
    property_type_id = fields.Many2one(
        'estate.property.type',
        related="property_id.property_type",
        store=True)

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        'Price must be positive'
    )

    @api.depends("date_deadline", "create_date")
    def _compute_validity(self):
        for record in self:
            start_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )

            if record.date_deadline:
                record.validity = (
                    record.date_deadline - start_date
                ).days
            else:
                record.validity = record.default_get(["validity"])["validity"]

    def _inverse_validity(self):
        for record in self:
            start_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def action_set_accepted(self):
        for record in self:
            property_record = record.property_id

            if record.state in ("accepted", "refused"):
                raise UserError(self.env._("This offer is already processed"))
            if property_record.offer_ids.filtered(lambda offer: offer.state == "accepted"):
                raise UserError(self.env._("An offer has already been accepted."))

            property_record.selling_price = record.price
            property_record.partner_id = record.partner_id
            record.state = "accepted"

            other_offers = property_record.offer_ids - record
            other_offers.write({"state": "refused"})
        return True

    def action_set_refused(self):
        for record in self:
            if record.state in ("accepted", "refused"):
                raise UserError(self.env._("This offer has already been processed."))
            record.state = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            the_property = self.env["estate.property"].browse(vals["property_id"])
            best_offer = max(the_property.offer_ids.mapped("price"), default=0)
            if best_offer >= vals["price"]:
                raise UserError("Cannot enter a new offer smaller than the best existing offer")
        offers = super().create(vals_list)

        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'

        return offers
