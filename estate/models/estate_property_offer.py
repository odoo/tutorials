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
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.state == 'new':
                property_id.state = 'offer_received'
            if property_id.offer_ids:
                if vals['price'] < property_id.offer_ids[0].price:
                    raise UserError("The offer price must be higher than the existing offer.")
        return super().create(vals_list)
        


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
