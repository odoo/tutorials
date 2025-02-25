# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class EstateProperties(models.Model):
    _inherit = "estate.properties"

    def action_property_sold(self):

        super().action_property_sold()
        whatsapp_composer = (
                self.env["whatsapp.composer"]
                .with_context({"active_id": self.id})
                .create(
                    {
                        "wa_template_id": self.env.company.wa_sale_template_id.id,
                        "res_model": "estate.properties",
                    }
                )
            )
        whatsapp_composer.sudo()._send_whatsapp_template(force_send_by_cron=True)

        
