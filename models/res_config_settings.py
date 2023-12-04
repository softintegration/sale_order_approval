# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_order_approval = fields.Boolean("Quotation Order Approval",
                                       default=lambda self: self.env.company.so_double_validation == 'two_step')
    so_double_validation = fields.Selection(related='company_id.so_double_validation', string="Levels of Approvals *",
                                            readonly=False)
    so_double_validation_amount = fields.Monetary(related='company_id.so_double_validation_amount',
                                                  string="Minimum Amount", currency_field='company_currency_id',
                                                  readonly=False)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.so_double_validation = 'two_step' if self.so_order_approval else 'one_step'