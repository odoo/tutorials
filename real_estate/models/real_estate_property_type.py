from odoo import api, fields, models


class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = "Real Estate Property Type"
    _sql_constraints = [
        ('unique_name', 'unique(name)', "A property type name must be unique.")
    ]
    _check_company_auto = True

    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many(
        string="Properties",
        comodel_name='real.estate.property',
        inverse_name='type_id',
        check_company=True,
    )
    average_price = fields.Float(string="Average Price", compute='_compute_average_price')
    company_id = fields.Many2one(
        string="Company", comodel_name='res.company', default=lambda self: self.env.company.id
    )

    # In practice, this computation will not work in all cases. It is merely given as an exercise to
    # understand the concept of multi-company, but it should not be used as-is in production.
    @api.depends('property_ids.selling_price')
    @api.depends_context('company')
    def _compute_average_price(self):
        for type in self:
            properties = type.property_ids.filtered(lambda p: p.company_id in self.env.companies)
            if properties:
                type.average_price = sum(properties.mapped('selling_price')) / len(properties)
            else:
                type.average_price = 0.0
