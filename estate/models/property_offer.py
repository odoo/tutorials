import datetime as dt
from math import floor

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Bids for a property"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(string="Validity of offer", default=7)
    date_deadline = fields.Date(string="Offer expiry", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    _check_positive_price = models.Constraint('CHECK(price >= 0)', 'Price has to be positive')

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Datetime.now(), days=record.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                raw_difference = record.date_deadline - (record.create_date or fields.Datetime.now()).date()
                difference = raw_difference.total_seconds()
                if difference > 0:
                    record.validity = floor(difference / dt.timedelta(days=1).total_seconds())

    @api.constrains('status')
    def _check_maximum_one_offer_accepted(self):
        accepted_offers = self.filtered(lambda r: r.status == "accepted")
        properties = accepted_offers.mapped('property_id')
        for property in properties:
            peer_offers = property.offer_ids
            accepted_peers = peer_offers.filtered(lambda r: r.status == 'accepted')
            if len(accepted_peers) > 1:
                raise ValidationError(_("A single offer can be accepted at a time!"))

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = self.env["estate.property"].browse(vals["property_id"] for vals in vals_list)
        # Precondition: price and property_id are required fields
        for vals in vals_list:
            property = property_ids.filtered(lambda p: p.id == vals["property_id"])
            property.ensure_one()
            # Hook-approach (for composability)
            property._set_offer_received()
            if property.best_price and property.best_price > vals['price']:
                raise UserError(_("New offer price must be higher than those of pre-existing offers!"))

        return super().create(vals_list)

    def action_confirm(self):
        for record in self:
            if record.status == "refused":
                raise UserError(_("Offer is already refused!"))

            record.status = 'accepted'
            record.property_id.confirm_offer()
        return True

    def action_cancel(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(_("Offer is already accepted!"))

            record.status = "refused"
        return True
