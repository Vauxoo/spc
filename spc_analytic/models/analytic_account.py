# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class AnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         'Account/Contract Name must be unique.'),
    ]
