from odoo import fields, models


class Student(models.Model):
    _name = "student.student"
    _description = "Student"

    name = fields.Char(required=True)
    age = fields.Integer()