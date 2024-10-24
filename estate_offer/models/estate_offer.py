from odoo import api, exceptions, fields, models


class Estate(models.Model):
    _name = "estate.property"
    _inherit = ["estate.property", "mail.thread"]

    offers_allowed = fields.Char(compute="_compute_offers_allowed")
    stage_reference = fields.Char(compute="_compute_stage_reference")
    has_accepted_offer = fields.Boolean(compute="_compute_has_accepted_offer")
    offer_ids = fields.One2many("estate.offer", inverse_name="estate_id")
    offers_amount = fields.Integer(compute="_compute_offers_amount")
    stage_id = fields.Many2one("estate.stage", required=True)

    @api.depends("stage_id")
    def _compute_stage_reference(self):
        for record in self:
            record.stage_reference = record.stage_id.reference

    def get_default_stage_id(self):
        return self.env.ref("estate.stage.to_publish")

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        for record in records:
            if not record.stage_id:
                record.stage_id = self.get_default_stage_id()
        return records

    @api.model
    def update(self, vals):
        record = super().update(vals)
        if not record.stage_id:
            record.stage_id = self.get_default_stage_id()

    @api.depends("offer_ids")
    def _compute_offers_amount(self):
        for record in self:
            record.offers_amount = len(self.offer_ids)

    @api.depends("offer_ids")
    def _compute_has_accepted_offer(self):
        for record in self:
            record.has_accepted_offer = bool(record.offer_ids.search([("is_accepted", "=", True)]))

    @api.constrains("offer_ids")
    def _check_unique_accepted_offer(self):
        if len([offer for offer in self.offer_ids if offer.is_accepted]) > 1:
            raise exceptions.UserError("There must be only one accepted offer.")

    @api.depends("stage_id")
    def _compute_offers_allowed(self):
        for record in self:
            negotiation_stage = self.env['estate.stage'].search([("reference", "=", "negotiation")], limit=1)
            record.offers_allowed = record.stage_id.order >= negotiation_stage.order if record.stage_id else False


class Offer(models.Model):
    _name = "estate.offer"
    _description = "This is the offer model."

    is_accepted = fields.Boolean(default=False, string="Accepted")
    amount = fields.Float(required=True)
    estate_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    buyer_id = fields.Many2one("res.users", required=True, ondelete="cascade")

    @api.constrains("amount")
    def _check_amount(self):
        if self.amount < 0:
            raise exceptions.UserError("The amount cannot be negative.")
        if self.amount <= self.estate_id.price:
            raise exceptions.UserError("The amount of the offer must be superior to the price of the estate.")


class Stage(models.Model):
    _name = "estate.stage"
    _description = "This is the stage models."

    reference = fields.Char(required=True)
    name = fields.Char(required=True)
    order = fields.Char(required=True)
