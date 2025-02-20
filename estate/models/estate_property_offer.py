from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7,)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id=fields.Many2one('estate.property.type', related="property_id.property_type_id", string="Property Type")

    _sql_constraints = [
        ("check_offer_price", "CHECK(price >= 0.0)",
         "The offer price should be strictly positive."),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            offers = self.env["estate.property"].browse(vals["property_id"]).offer_ids
            if len(offers) > 0 and min([offer.price for offer in offers]) > vals["price"]:
                raise exceptions.ValidationError("The offer price can't be lower than another existing offer")
            if self.env["estate.property"].browse(vals["property_id"]).status == "new":
                self.env["estate.property"].browse(vals["property_id"]).status = "offer_received"
        return super().create(vals_list)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)

    def accept_offer(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise exceptions.UserError("More than one offer can't be accepted for the same property")
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.status = "offer_accepted"
        return True

    def refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
