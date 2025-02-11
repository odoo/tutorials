from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property Offers"
    _order = "price desc"
    price = fields.Integer()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7, store=True)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    create_date = fields.Date(default=fields.Datetime.today())
    _sql_constraints = [
        ("positive_price", "CHECK(price > 0)", "Expected price cannot be negative.")
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date
            record.validity = delta.days

    def action_confirm(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer accepted"
        return True

    def action_cancel(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        if isinstance(vals_list, list):
            for vals in vals_list:
                property_id = vals.get("property_id")
                if property_id:
                    property_record = self.env["estate.property"].browse(property_id)
                    if property_record:
                        property_record.write({"state": "offer received"})

                if vals["price"] is not None:
                    highest_price = property_record.best_price
                    if vals["price"] < highest_price:
                        raise UserError(
                            f"Error: the price cannot be less than maximum price {highest_price}."
                        )
        else:
            property_id = vals.get("property_id")
            if property_id:
                property_record = self.env["estate.property"].browse(property_id)
                if property_record:
                    property_record.write({"state": "offer received"})

            if vals["price"] is not None:
                highest_price = property_record.best_price
                if vals["price"] < highest_price:
                    raise UserError(
                        f"Error: the price cannot be less than maximum price {highest_price}."
                    )
        return super().create(vals)
