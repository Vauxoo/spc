# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"
    _name = "res.company"

    authorized_range = fields.Char('Authorized range', size=128)
    cai = fields.Char('C.A.I', size=128)
    date_issue = fields.Date('Date of issue')
