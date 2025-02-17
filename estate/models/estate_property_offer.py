from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer_model"
    _description = "hiiii"
    _order = "price desc"

    ###### sql constrains ######
    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "Offer price must be strictly positive")
    ]
    
    ###### fiels #########
    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_model', required=True)
    property_type_id = fields.Many2one("estate_property_type_model", name="Property Type", related='property_id.property_type_id')
    create_date = fields.Datetime(default=fields.Date.today(), readonly=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    ###### compute methods #####
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                deadline = fields.Datetime.from_string(record.create_date) + timedelta(days=record.validity)
                record.date_deadline = deadline.date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date)
                validity = (fields.Datetime.from_string(record.date_deadline) - create_date).days
                record.validity = validity
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate_model"].browse(vals.get("property_id"))
            if not property_id:
                    raise UserError("Property must be specified for an offer.")
            if property_id.offer_ids and vals["price"] <= max(property_id.offer_ids.mapped("price")):
                    raise UserError("You cannot create an offer lower than an existing offer!")
        property_id.state = "offer_received"
        return super(EstatePropertyOffer, self).create(vals_list)

    def action_accept(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("this offer is allready acceplted")

            existing_record = self.search([("property_id", "=", record.property_id.id), ("status", "=", "accepted")], limit=1)
            if existing_record:
                raise UserError("another offer is already accepted")

            record.status = "accepted"
            record.property_id.write({
                "buyer" : record.partner_id.id,
                "selling_price" : record.price,
                "state" : "offer_accepted"
            })
        return True
    
    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("offer is already accepted thats why you cant refuse it")
            record.status = "refused"
        return True