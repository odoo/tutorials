from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    deadline_date = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("property_id.create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.property_id.create_date:
                record.deadline_date = record.property_id.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.deadline_date = False

    def _inverse_deadline(self):
        for record in self:
            if record.property_id.create_date and record.deadline_date:
                flag = fields.Date.from_string(record.deadline_date)
                flag1 = fields.Date.from_string(record.property_id.create_date)
                if flag and flag1:
                    record.validity = (flag - flag1).days
                else:
                    record.validity = 7
            else:
                record.validity = 7

    def action_refused(self):
        for record in self:
            record.status = "refused"

    def action_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    _sql_constraints = [
        ("price", "CHECK(price >= 0)", "A price must be strictly positive.")
    ]
    # @api.constrains('property_id.bedrooms')
    # def _check_bedrooms(self):
    #     for record in self:
    #         if record.property_id.bedrooms < 0:
    #             raise ValidationError("You have to set bedrooms")
