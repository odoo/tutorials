from odoo import fields, models, api, tools, exceptions
from dateutil.relativedelta import relativedelta


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "You receive: Northing. I receive: a goddamn house."
    _order = "price desc"
    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id")
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must not be negative")
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if (not record.create_date):
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)
                continue
            record.date_deadline = relativedelta(days=record.validity) + record.create_date

    def _inverse_date_deadline(self):
        for record in self:
            if (not record.create_date):
                record.validity = record.date_deadline - fields.Date.now()
                continue
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accept(self):
        for record in self:
            record.status = "accepted"
            re_property = record.property_id
            re_property.selling_price = record.price
            re_property.state = "offer_accepted"
            re_property.customer_id = record.partner_id

    def action_offer_refuse(self):
        for record in self:
            record.status = "refused"
            
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env["estate.property"].browse(vals["property_id"]).state == "offer_received":
                if tools.float_utils.float_compare(self.env["estate.property"].browse(vals["property_id"]).best_price, vals["price"], precision_digits=10) == 1:
                    raise exceptions.UserError("Offer cannot be lower than current best price.")
            else:
                self.env["estate.property"].browse(vals["property_id"]).state = "offer_received"
        return super().create(vals)
