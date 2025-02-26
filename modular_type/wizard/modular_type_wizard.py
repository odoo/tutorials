# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ModularTypesWizard(models.TransientModel):
    _name = "modular.type.wizard"
    _description = "Wizard to set Modular Types"

    modular_types = fields.Many2many(
        "modular.types",
        string="Modular Types"
    )

    def default_get(self, fields_list):
        res = super(ModularTypesWizard, self).default_get(fields_list)
        active_id = self._context.get("active_id")

        if active_id:
            order_line = self.env["sale.order.line"].browse(active_id)

            if order_line.product_id:
                modular_types = order_line.product_id.product_tmpl_id.modular_types
                res["modular_types"] = [(6, 0, modular_types.ids)]

        return res
