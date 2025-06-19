from odoo import fields, models, api


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name"
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'the type name must be unique')
    ]

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_view_offers(self):
        res = self.env.ref("estate.estate_property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res
