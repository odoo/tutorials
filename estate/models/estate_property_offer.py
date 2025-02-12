from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the estate property offer model"
    _order = "price desc"


    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True, ondelete="cascade")
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type", compute="_compute_property_type_id", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        offers = super().create(vals_list)
        print(offers)
        for offer in offers:
            print(offer)
            property_obj = offer.property_id
            print(property_obj)
            max_existing_offer = max(property_obj.offer_ids.mapped("price"), default=0)
            if offer.price < max_existing_offer:
                raise UserError(f"The offer price should be greater than {max_existing_offer}.")
            if property_obj.state == 'new':
                property_obj.state = 'offer_received'
        return offers


    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "The offer price must be greater than 0")
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    @api.depends("property_id.property_type_id")
    def _compute_property_type_id(self):
        for record in self:
            record.property_type_id = record.property_id.property_type_id

    def action_offer_accepted(self):
        for record in self:
            if record.property_id:
                if record.status == "accepted" or record.property_id.state == "offer_accepted":
                    raise UserError("The offer is already accepted!!!")
                else:
                    record.status = "accepted"
                    record.property_id.state = "offer_accepted"
                    record.property_id.buyer_id = record.partner_id
                    record.property_id.selling_price = record.price

    def action_offer_refused(self):
        for record in self:
            if record.property_id:
                if record.status == "refused":
                    raise UserError("The offer is already refused!!!")
                else:
                    record.status = "refused"
