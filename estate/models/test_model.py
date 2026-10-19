# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model for Tutorials"

    name = fields.Char()