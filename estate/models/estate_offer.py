from datetime import timedelta

from odoo.exceptions import UserError

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("new", "New")
        ],
        copy=False,
        default="new"
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_dead_line", inverse="_inverse_validity")

    _check_positif_price = models.Constraint(
        'CHECK(price > 0)',
        'The price must be positive'
    )

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            property.set_offer_received()
            all_prices = property.proterty_offer_ids.mapped('price')
            max_price = all_prices[0] if all_prices else 0
            if max_price and max_price >= vals['price']:
                raise UserError(self.env._("New offer can't be lower than an other offer"))
        return super().create(vals_list)

    @api.depends("validity")
    def _compute_dead_line(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_validity(self):
        for offer in self:
            difference = (offer.create_date.date() - fields.Date.today())
            offer.validity = difference.days

    def action_accept_offer(self):
        for offer in self:
            if offer.status == "refused":
                raise UserError(self.env._("Can't accept an refused offer"))
            offer.status = "accepted"
            offer.property_id.accept_offer()
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError(self.env._("Can't refuse an accepted offer"))
            offer.status = "refused"
        return True
