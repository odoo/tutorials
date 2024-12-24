from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for real state properties"
    _order = "price desc"


    validity = fields.Integer(string="Validity (Days)", default=7)

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    property_id = fields.Many2one(comodel_name="estate.property")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Buyer")

    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    _sql_constraints = [
        ("check_price", "CHECK(price >= 0)", "Offer prices MUST be postive."),
    ]

    def action_accept(self):
        self.ensure_one()
        self.property_id.action_process_accept(self)
        self.status = "accepted"
        return True


    def action_refuse(self):
        self.ensure_one()
        self.status = "refused"
        return True

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days


    @api.model_create_multi
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals['property_id'])
        existing_offers = self.search([
            ('property_id', '=', vals['property_id'])
        ])
        if any(offer.price >= vals['price'] for offer in existing_offers):
            raise ValidationError(
                "Error, You CANNOT create an offer with a lower price than an existing one."
            )
        property_record.state = 'offer_received'
        return super().create(vals)
