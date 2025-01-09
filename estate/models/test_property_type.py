from odoo import models,fields,api

class TestPropertyType(models.Model):
    _name = "test.property.type"
    _description = "Test proerty Type"

    _order = "name"

    name = fields.Char('name')
    propertys_id = fields.One2many("test.property", "property_types_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order type")
    offer_ids = fields.One2many('test.property.offer', 'property_type_id', string='offers')
    offer_count = fields.Integer(readonly=True,compute="_compute_count_offer")

    @api.depends('offer_ids')
    def _compute_count_offer(self):
        for record in self:
            record.offer_count = len(self.offer_ids)


    _sql_constraints = [
        ("name_uniq", "unique(name)", "Type must be unique"),
    ]