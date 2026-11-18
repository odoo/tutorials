from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.profiler import Profiler


class PropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "this model is used to define the offers received to the property"
    _order = "price desc"

    def _cal_deadline(self):
        return fields.Date.today() + relativedelta(days=7)

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], default=False, copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        "estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    deadline = fields.Date(
        default=_cal_deadline,
        copy=False,
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True,
    )
    validity_days = fields.Integer(default=7, copy=False)

    _check_price = models.Constraint(
        "check(price>0)", "Offer price must be strictly positive"
    )

    @api.depends("validity_days")
    def _compute_deadline(self):
        for records in self:
            base_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            records.deadline = base_date + \
                relativedelta(days=records.validity_days)

    def _inverse_deadline(self):
        for records in self:
            base_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            diff = relativedelta(records.deadline, base_date)
            records.validity_days = diff.days

    def action_confirm(self):
        with Profiler():
            offers = self.property_id.offer_ids.filtered(
                lambda r: r.id != self.id)
            offers.status = "refused"
            self.status = "accepted"
            self.property_id.write({
                'state': 'offer_accepted',
                'buyer_id': self.partner_id.id,
                'selling_price': self.price
            })
            self.property_id.flush_recordset(['state'])

    def action_cancel(self):
        for rec in self:
            rec.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list:
            property_id = self.env["estate.property"].browse(
                vals_list[0].get("property_id")
            )
            best_price = property_id.best_price

            for vals in vals_list:
                if vals["price"] < best_price:
                    raise ValidationError(
                        "Can't add this offer, price is lower than an existing offer."
                    )

            property_id.state = "offer_received"
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_offer(self):
        if len(self) == len(self.property_id.offer_ids):
            self.property_id.state = "new"
