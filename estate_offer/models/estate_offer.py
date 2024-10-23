from odoo import api, exceptions, fields, models


class Estate(models.Model):
    _inherit = "estate.estate"

    accept_offers = fields.Boolean(default=True)
    has_accepted_offer = fields.Boolean(compute="_compute_has_offer")
    offer_ids = fields.One2many("estate.offer", inverse_name="estate_id")
    len_offers = fields.Integer()

    @api.depends("offer_ids")
    def _computed_len_offer(self):
        for record in self:
            record.len_offers = len(self.offer_ids)

    @api.depends("offer_ids")
    def _compute_has_offer(self):
        for record in self:
            record.has_accepted_offer = any([offer.is_accepted for offer in self.offer_ids])

    @api.constrains("offer_ids")
    def _check_unique_accepted_offer(self):
        if len([offer for offer in self.offer_ids if offer.is_accepted]) > 1:
            raise exceptions.UserError("There must be only one accepted offer.")


class Offer(models.Model):
    _name = "estate.offer"
    _description = "This is the offer model."

    is_accepted = fields.Boolean(default=False, string="Accepted")
    amount = fields.Float(required=True)
    estate_id = fields.Many2one("estate.estate", required=True)
    user_id = fields.Many2one("res.users", required=True)

    @api.constrains("amount")
    def _check_amount_superior_zero(self):
        minimal_value = 0
        if self.amount < minimal_value:
            raise exceptions.UserError(f"The amount of the offer must not be inferior to {minimal_value}")

    @api.constrains("amount")
    def _check_amount_superior_estate_price(self):
        print(self.estate_id.price)
        if self.amount <= self.estate_id.price:
            raise exceptions.UserError("The amount of the offer must be superior to the price of the estate.")
