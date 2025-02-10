from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order="sequence, name"


    name = fields.Char("Name", required=True)
    sequence=fields.Integer("sequence", default=1)
    property_ids=fields.One2many("estate.property","property_type_id", string="properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    property_count = fields.Integer(compute="_compute_property_count")

    _sql_constraints = [
        ("unique_name","UNIQUE(name)","property type must be the unique")
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def _compute_property_count(self):
        for record in self:
            record.property_count = self.env["estate.property"].search_count([("property_type_id", "=", record.id)])

    def action_display_property(self):
        related_property_ids = (self.env["estate.property"].search([("property_type_id", "=", self.id)]).ids)
        return {
            "type": "ir.actions.act_window",
            "name": ("Properties"),
            "res_model": "estate.property",
            "views": [[False, "list"], [False, "form"]],
            "domain": [("id", "in", related_property_ids)],
        }