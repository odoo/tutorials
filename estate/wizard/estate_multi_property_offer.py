from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateMultiPropertyOffer(models.TransientModel):
    _name = 'estate.multi.property.offer'
    _description = 'Multi property offers'

    price = fields.Float()
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one(
        "estate.property", ondelete="cascade")
    deadline = fields.Date(
        default=lambda _: fields.Date.today() + relativedelta(days=7),
        copy=False,
        store=True,
    )
    validity_days = fields.Integer(default=7, copy=False)

    def action_multi_property_offer(self):
        active_ids = self.env.context.get('active_ids')
        offers_vals_list = [{
            'price': self.price,
            'partner_id': self.partner_id.id,
            'property_id': rec_id,
            'deadline': self.deadline,
            'validity_days': self.validity_days
        } for rec_id in active_ids]

        return self.env['estate.property.offers'].create(offers_vals_list)
