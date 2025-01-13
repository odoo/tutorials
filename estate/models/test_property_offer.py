from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class test_property_offer(models.Model):
    _name = "test.property.offer"
    _description = "Test proerty Offer"

    _order = "price desc"

    price = fields.Float("price", required=True)
    status = fields.Selection(
        [("Accepted", "Accepted"), ("Refused", "Refused"), ("Pending", "Pending")],
        default="Pending",
        copy=False,
    )
    buyer_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("test.property", required=True, ondelete="cascade")
    #! if there is compute and inverse in model then both fields data have to give in demo data
    # ! can't call compute or inverse if there is any default given in any feld
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        default=datetime.today(),
    )
    property_type_id = fields.Many2one(
        related="property_id.property_types_id", string="property_type"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                datetime.today() + relativedelta(days=record.validity)
            ).date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - datetime.today().date()).days
            else:
                record.date_deadline = 0

    def property_accepted(self):
        for record in self:
            if record.property_id.status != "offer_accepted"    :
                if record.status == "Pending":
                    record.status = "Accepted"
                    record.property_id.selling_price = record.price
                    record.property_id.buyer_id = record.buyer_id
                    record.property_id.status = "offer_accepted"

            else:
                raise UserError(" offer already accepted")

    def property_rejected(self):
        for record in self:
            if record.property_id.status != "cancelled":
                if record.status == "Accepted" or record.status == "Pending":
                    if record.status == "Accepted":
                        record.property_id.selling_price = 0
                    record.status = "Refused"
                    record.property_id.status = "offer_received"

                else:
                    record.status = "Pending"

    @api.constrains("price", "status")
    def _check_offer_constraint(self):
        for record in self:
            if (
                record.price / record.property_id.expected_price * 100
            ) < 90 and record.status == "Accepted":
                raise ValidationError(
                    "The selling price must be atleast 90 percentage of expected price"
                )

        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals["property_id"]:
                prop = self.env["test.property"].browse(vals["property_id"])
            if vals["price"] < prop.best_price:
                raise UserError("price must be greater than best price")
            if prop.status == "new":
                prop.status = "offer_received"
        return super().create(vals_list)

    # @api.model
    # def create(self , vals_list):
    #     prop = self.env["test.property"].browse(vals_list["property_id"])
    #     if vals_list["price"] < prop.best_price:
    #         raise UserError('price must be greater than best price')
    #     if prop.status == "new":
    #         prop.status = "offer_received"
    #     return super().create(vals_list)
