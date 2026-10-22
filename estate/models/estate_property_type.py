# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate property type"
    _order = "sequence asc"

    _name_uniq = models.Constraint(
        'UNIQUE(name)',
        'The type name must be unique.',
    )

    name = fields.Char('Type name', required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer("Sequence", default=1)
    property_count = fields.Integer(compute="_compute_property_count")
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_type_id', string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "estate.property",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id}
        }

    def action_open_offer_ids(self):
        return {
            "name": _("Related Offers"),
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "estate.property.offer",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id}
        }
