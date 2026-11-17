from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string="Property",
        required=True,
        index=True,
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            start = offer._get_start_date()
            offer.date_deadline = fields.Date.add(start, days=offer.validity)

    def _inverse_date_deadline(self):
        """Derive the validity in days from the deadline entered by the user."""
        for offer in self.filtered('date_deadline'):
            start = offer._get_start_date()
            offer.validity = (offer.date_deadline - start).days

    def _get_start_date(self):
        """Return the creation date, or today while the offer is not saved yet."""
        self.ensure_one()
        return self.create_date.date() if self.create_date else fields.Date.today()
