from odoo import api, fields, models
from datetime import timedelta, date
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Ayve"
    _order = "price desc"
    _sql_constraints = [
        (
            "check_offerprice_not_negative",
            "CHECK(price >= 0.0)",
            "The Offer Price should be greater than 0.",
        ),
    ]

    price = fields.Float()
    status = fields.Selection(
    [
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ],
    string='Status',
    copy=False
    )

    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string="Partner"
    )

    property_id = fields.Many2one(
        'estate.property',
        required=True,
        string="Property ID"
    )

    property_type_id = fields.Many2one(related="property_id.property_type_id", store="True")

    validity = fields.Integer(
        string="Validity(Days)",
        default=7
    )

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True
    )

    # Compute Methods
    # when inverse is used the field becomes editable (not read only)
    # compute makes it read only
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = date.today()
            record.date_deadline = record.create_date.date() + timedelta(days=record.validity)

    # used the abs so the app wont crash when getting -ve number
    def _inverse_deadline(self):
        for record in self:
            record.validity = abs((record.date_deadline - record.create_date.date()).days)

    def action_accept_offer(self):
        for record in self:
            if (record.property_id.buyer_id):
                if (record.partner_id != record.property_id.buyer_id):
                    raise UserError("This Property has already accepted an offer.")
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = False
            record.status = 'refused'
        return True

    @api.model
    def create(self, offer):
        property_id = self.env["estate.property"].browse(offer["property_id"])
        if offer["price"] < property_id.best_price:
            raise UserError("Offer price must be higher than existing offer.")
        property_id.state = "offer_received"
        return super().create(offer)
