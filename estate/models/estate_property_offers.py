from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "this model is used to define the offers received to the property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused"), ("pending", "Pending")],
        default="pending",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        "estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related="property_id.property_type_id")
    deadline = fields.Date(
        default=lambda self: fields.Date.today() + relativedelta(days=7),
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
        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        offers = self.env["estate.property.offers"].browse(
            self.env["estate.property.offers"].search([]).ids
        )
        for record in offers:
            if record.id != self.id:
                record.status = "refused"

    def action_cancel(self):
        for rec in self:
            if rec.status == "accepted" and rec.property_id.state == "sold":
                raise ValidationError("Sold property cannot be refused")
            rec.status = "refused"

    @api.ondelete(at_uninstall=False)
    def _unlink_if_sold(self):
        for rec in self:
            if rec.property_id.state == "sold" and rec.status == "accepted":
                raise ValidationError("Sold property cannot de removed")
