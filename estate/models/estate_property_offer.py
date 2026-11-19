from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer._get_start_date() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer._get_start_date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env["estate.property"].browse(vals["property_id"])
            if float_compare(
                vals.get("price", 0.0), estate_property.best_price, precision_digits=2
            ) < 0:
                raise UserError(self.env._(
                    "The offer must be higher than %s.", estate_property.best_price
                ))
            estate_property.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            if "accepted" in offer.property_id.offer_ids.mapped("status"):
                raise UserError(self.env._(
                    "An offer has already been accepted for this property."
                ))
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    def _get_start_date(self):
        """Return the date from which the validity is counted.

        The creation date is only set once the offer is saved, so today's
        date is used as a fallback for offers being created.
        """
        self.ensure_one()
        return self.create_date.date() if self.create_date else fields.Date.today()
