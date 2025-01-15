from datetime import datetime, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", required=True, string="Partner"
    )
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer Price must be positive.")
    ]

    @api.constrains("price")
    def _check_offer_price(self):
        for record in self:
            if record.property_id.offer_ids and any(
                offer.price >= record.price
                for offer in record.property_id.offer_ids
                if offer.id != record.id
            ):
                raise ValidationError(
                    "You cannot create an offer lower than an existing offer."
                )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date + timedelta(days=record.validity)
                ).date()
            else:
                record.date_deadline = (
                    datetime.today() + timedelta(days=record.validity)
                ).date()

    @api.model_create_multi
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.ondelete(at_uninstall=False)
    def _unlink_except_accepted_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Accepted offers cannot be deleted.")

    def action_offer_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "accepted"

            # set status 'refused' in the other offers of that particular property
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = "refused"
        return True

    def action_offer_refused(self):
        for record in self:
            record.status = "refused"
        return True
