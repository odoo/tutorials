from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'An offer price must be strictly positive')
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)")
    deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - fields.Date.today()).days

    def action_accept(self):
        if 'accepted' in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer is already accepted")
        else:
            for record in self:
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, values):
        for vals in values:
            if vals.get("property_id") and vals.get("price"):
                prop = self.env["estate.property"].browse(vals["property_id"])
                if prop.offer_ids:
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                        raise UserError(f"The offer must be higher than {max_offer}")
                prop.state = "offer_received"
        return super().create(values)
