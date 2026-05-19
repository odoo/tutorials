from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"
    _check_price_positive = models.Constraint("CHECK (price >= 0)", "Offer price must be strictly positive.")

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        readonly=False,
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price"):
                prop = self.env["estate.property"].browse(vals["property_id"])
                if prop.offer_ids:
                    highest_offer = max(prop.mapped("offer_ids.price"))
                    if float_compare(vals["price"], highest_offer, precision_rounding=0.01) <= 0:
                        raise UserError(_("The offer must be higher than %(offer)s.", offer=highest_offer))
                prop.state = "offer_received"
        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = ((record.date_deadline or fields.Date.today()) - record.create_date.date()).days

    def action_status_accepted(self):
        if self.property_id.state in ("new", "offer_received"):
            self.status = "accepted"
            self.property_id.state = "offer_accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
        else:
            raise UserError(_("This property has already accepted an offer, been sold, or is cancelled!"))
        return True

    def action_status_refused(self):
        self.status = "refused"
        return True
