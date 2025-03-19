from odoo import api, exceptions, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name asc" 

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    # offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    sequence = fields.Integer("Sequence", default=10)

    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count"
    )

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    @api.depends('offer_ids.property_id.property_type_id')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['estate.property.offer'].search_count([
                ('property_id.property_type_id', '=', record.id)
            ])

    # @api.depends("offer_ids","offer_ids.property_id")
    # def _compute_offer_count(self):
    #     for record in self:
    #         record.offer_count = len(record.offer_ids)    
    # ##(why this code is not running and above code is running !!)
