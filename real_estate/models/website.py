# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class Menu(models.Model):
    _inherit = 'website.menu'

    @api.model
    def create_properties_menu(self):

        contact_menu = self.search([('name', '=', 'Contact Us')], limit=1)
        if contact_menu:
            self.create({
                'name': 'Properties',
                'url': '/properties',
                'parent_id': contact_menu.parent_id.id,
                'sequence': contact_menu.sequence + 1,
                'website_id': contact_menu.website_id.id,
            })
