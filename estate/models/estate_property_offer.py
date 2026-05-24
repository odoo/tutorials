from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _inherit = ["mail.activity.mixin", "mail.thread.main.attachment"]

    name = fields.Char(string="Property Offer", required=True)
    price = fields.Integer(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        readonly=False,
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.model
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])
            if property.best_price > val.get("price", 0):
                raise UserError("Better offer than this already exist")
            property.state = "offer_received"
        return super().create(vals)

    @api.model
    def _crone_refuse_offer(self):
        offer = self.search([])
        for i in offer:
            if (
                i.date_deadline < fields.Date.today() or i.validity < 0
            ) and i.status != "accepted":
                i.status = "refused"

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for records in self:
            default_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            records.date_deadline = fields.Date.add(default_date, days=records.validity)

    def _inverse_deadline(self):
        for records in self:
            default_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            if records.date_deadline:
                records.validity = (records.date_deadline - default_date).days

    def activity_update(self):
        activity_vals = []
        for record in self:
            if record.status == "accepted":
                note = "Property offer accepted"
                activity_type = self.env.ref("mail.mail_activity_data_todo")
                date_deadline = fields.Date.add(record.create_date, months=1)
                res_model_id = self.env["ir.model"]._get_id("estate.property")
                activity_vals.append(
                    {
                        "activity_type_id": activity_type.id,
                        "automated": True,
                        "date_deadline": date_deadline,
                        "note": note,
                        "user_id": record.property_id.sales_person.id,
                        "res_id": record.property_id.id,
                        "res_model_id": res_model_id,
                    }
                )

        self.env["mail.activity"].create(activity_vals)

    def save_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Offer is already accepted")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "accepted"
            record.activity_update()

    def cancel_offer(self):
        for record in self:
            if record.status != "accepted" or record.status != "refused":
                record.status = "refused"
                if record.property_id.buyer_id == record.partner_id:
                    record.property_id.selling_price = False
                    record.property_id.state = False

    _check_price = models.Constraint(
        "CHECK(price >= 0)", "Price filled must be positive"
    )
