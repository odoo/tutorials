from dateutil.relativedelta import relativedelta

from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for an estate property"
    _check_price = models.Constraint("CHECK(price > 0)", "The offer must be positive")
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    create_date = fields.Date(default=fields.Date.today())
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env["estate.property"].browse(vals["property_id"])
            if vals["price"] <= estate_property.best_price:
                raise exceptions.UserError(f"The offer must be higher than {estate_property.best_price}")
            if estate_property.state == "new":
                estate_property.state = "offer_received"
        return super().create(vals_list)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    def action_accept(self):
        for record in self:
            if record.property_id.selling_price:
                raise exceptions.UserError("An other is already accepted")
            else:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
