# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare, float_round

APPROVAL_REQUEST_ACCEPTED_STATES = ('draft',)

class SaleOrder(models.Model):
    _inherit = "sale.order"


    state = fields.Selection([
        ('draft', 'Quotation'),
        ('awaiting_approval', 'Awaiting Approval'),
        ('approved_quotation', 'Approved quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    require_approval = fields.Boolean(compute='_compute_require_approval')

    @api.depends('company_id.so_double_validation')
    def _compute_require_approval(self):
        for each in self:
            # FIXME: Here we have use a static precision_digits as it is the value used in all the checks of the monetary fields in sale module
            each.require_approval = each.company_id.so_double_validation == 'two_step' and \
            float_compare(each.amount_total, each.company_id.so_double_validation_amount, precision_digits=2) >= 0


    def action_approval_request(self):
        if not self._check_approval_request():
            raise ValidationError(_("Some Quotation state doesn't allow to request approval!"))
        self._action_approval_request()

    def _check_approval_request(self):
        approval_request_accepted_states = tuple(set(self.mapped("state")).union(set(APPROVAL_REQUEST_ACCEPTED_STATES)))
        if approval_request_accepted_states != APPROVAL_REQUEST_ACCEPTED_STATES:
            return False
        return True


    def _action_approval_request(self):
        self.write({'state':'awaiting_approval'})

