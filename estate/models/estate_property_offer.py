from odoo import api, exceptions, fields, models
from odoo.tools import float_utils
from odoo.tools.translate import _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(string="Status", copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(related="property_id.property_type_id", stored=True)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "The offer price must be strictly positive")
    ]
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date().add(offer.create_date.date(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_offer_accepted(self):
        if float_utils.float_is_zero(self.property_id.selling_price, 2):
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            return True
        else:
            raise exceptions.UserError(_("An offer has already been accepted."))

    def action_offer_refused(self):
        if not self.status:
            self.status = "refused"
            return True
        else:
            raise exceptions.UserError(_("You can't refuse an accepted offers"))
