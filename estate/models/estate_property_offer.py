# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer's"
    _order = "price desc"
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Offer Price Must be Positive Value')
    ]

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(
        comodel_name="estate.property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", related="property_id.property_type_id", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date
                    + fields.date_utils.relativedelta(days=record.validity)
                )
            else:
                record.date_deadline = (
                    fields.Datetime.now()
                    + fields.date_utils.relativedelta(days=record.validity)
                )

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.valpassidity = (record.date_deadline -
                                       fields.Datetime.now()).days

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property = self.env["estate.property"].browse(
                record["property_id"])

            if record['price'] < property.best_price:
                raise UserError(
                    _("The Offer must higher then %s for %s Property", property.best_price, property.name))
            elif property.state == "sold":
                raise UserError(_("Property Already Sold"))

            property.state = "offer received"

            property.message_post({'body': _(
                "offer created with Price %s by %s", record['price'], record['partner_id'])})

        return super().create(vals)

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == "offer accepted":
                raise UserError(
                    _("An offer Already Accepted for this Property"))

        if self.status == "accepted":
            raise UserError(
                _("You can't Accept an offer it's already %s", self.status.capitalize()))
        elif self.property_id.state == "sold":
            raise UserError(_("Property Already Sold"))

        self.property_id.state = "offer accepted"
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.property_buyer_id = self.partner_id.id
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        if self.status == "refused":
            raise UserError(
                _("You can't Refuse an offer it's already %s", self.status.capitalize()))
        elif self.status == "accepted":
            self.property_id.state = "offer received"
            self.property_id.selling_price = None
            self.property_id.property_buyer_id = None

        self.status = "refused"
        return True
