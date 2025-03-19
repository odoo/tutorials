from odoo import api,fields, models,exceptions

class Inheritance0(models.Model):
    _name = 'inheritance.0'
    _description = 'Inheritance Zero'

    name = fields.Char()

    def call(self):
        return self.check("model 0")

    def check(self, s):
        return "This is {} record {}".format(s, self.name)

class Inheritance1(models.Model):
    _name = 'inheritance.1'
    _inherit = 'inheritance.0'
    _description = 'Inheritance One'

    family_name=fields.Char()

    def call(self):
        return self.check("model 1")

class Inheritance2(models.Model):
    _name = 'inheritance.2'
    _inherits = {'inheritance.0':'inher0_id'}
    _description = 'Inheritance two'
    
    inher0_id=fields.Many2one("inheritance.0",required=True,ondelete="cascade")

    address=fields.Char()

    def call(self):
        return self.check("model 1")
