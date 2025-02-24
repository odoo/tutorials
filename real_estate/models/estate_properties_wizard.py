# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models
from odoo.exceptions import UserError


class EstatePropertiesWizard(models.TransientModel):
    _name = 'estate.properties.wizard'
    _description = 'Wizard model for saving multiple offer records.'

    price = fields.Float(required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Buyer', index=True, copy=False, required=True)

    def action_select_offer(self):
        properties = self.env['estate.properties'].browse(
            self._context.get('active_ids'))
        property_arr = []
        for property_data in properties:
            if (property_data.state not in ['new', 'offer_recieved']):
                raise UserError(
                    _('One or more property is either sold or in accepted state.'))
            data = {
                "price": self.price,
                "property_id": property_data.id,
                "partner_id": self.partner_id.id,
            }
            property_arr.append(data)

        self.env["estate.properties.offer"].create(
            property_arr
        )
        properties.write({'state': 'offer_recieved'})
