from odoo import fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Command, Domain
from odoo.http import Controller, route, request

class EstateProperty(Controller):
    @route(['/properties'], type='http', auth='public', website=True)
    def properties(self):
        all_properties = request.env['estate.property'].search([])
        return request.render("estate.estateproperties",{'properties': all_properties})