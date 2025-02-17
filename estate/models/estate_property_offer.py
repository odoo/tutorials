from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    _order = "price desc"
    price = fields.Float(string="Offer Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Offer Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (in days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_validity", store=True)
    create_date = fields.Date(readonly=True, default=fields.Date.today)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", related='property_id.property_type_id', store=True)  # related field: Automatically fetches the property type.


    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity is not None:
                record.date_deadline = datetime.now().date() + timedelta(days=record.validity)
            else:
                # If validity is not set, set the deadline to 7 days
                record.date_deadline = datetime.now().date() + timedelta(days=7)

    def _inverse_validity(self):
            for record in self:
                if record.create_date and record.date_deadline:
                    record.validity = (record.date_deadline - record.create_date).days



    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_offer_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id),
                ('status', '!=', 'refused')
            ])
            other_offers.write({'status': 'refused'})
        return True

    def action_offer_refuse(self):
        self.status = "refused"
        return True


    # -------------------------------------------------------------------------
    # SQL CONSTRAINTS QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price must be positive'),
    ]

    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            offer_price = vals.get('price')
            current_maximum_offer = self.search([('property_id', '=', vals['property_id'])], order="price desc", limit=1) # Fetch the current maximum offer for the property, already stored in the descending order of price.

            if offer_price < current_maximum_offer.price:
                raise UserError(f"The offer price must be higher than {current_maximum_offer.price}")
            else:
                offer_reccived_property = self.env['estate.property'].browse(vals.get('property_id'))
                offer_reccived_property.state = "offer_received"

        return super().create(vals_list)
