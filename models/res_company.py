# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'


    so_double_validation = fields.Selection([
        ('one_step', 'Confirm Quotation orders in one step'),
        ('two_step', 'Get 2 levels of approvals to confirm a Quotation order')
        ], string="Levels of Approvals", default='one_step',
        help="Provide a double validation mechanism for Quotations")

    so_double_validation_amount = fields.Monetary(string='Double validation amount', default=5000,
        help="Minimum amount for which a double validation is required")
