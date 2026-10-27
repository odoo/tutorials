from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property ofer"
    _order = "price desc"

    price = fields.Float('Price', default=0)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    validity = fields.Integer(string='Offer Validity', default=7)
    date_deadline = fields.Date('Offer Deadline', compute='_compute_validity', inverse='_inverse_validity')
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    _check_offer_price = models.Constraint(
        'CHECK(price >= 0)',
        'The offer price cannot be negative',
    )

    @api.depends('validity', 'create_date')
    def _compute_validity(self):
        for record in self:
            base_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date
            else:
                create_date = fields.Date.today()
            # record.validity = (record.date_deadline - create_date).days
            create_date_val = create_date.date() if hasattr(create_date, 'date') else create_date
            record.validity = (record.date_deadline - create_date_val).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                UserError('Property was already sold')
            if record.property_id.state == 'cancelled':
                UserError('Cancelled properties cannot be sold')
            else:
                record.status = 'accepted'
                record.property_id.state = 'offeraccepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0.0)
            prop = self.env["estate.property"].browse(property_id)
            maxprice = max(prop.offer_ids.mapped("price"), default=0.0)
            if price <= maxprice:
                raise UserError("New offer must be higher than all other already existing offers")
        prop.state = 'offerreceived'
        return super().create(vals_list)
