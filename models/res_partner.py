from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'
    _description = 'The customer'

    account_ids = fields.One2many("knance.account", "customer_id", string="Vos comptes")
    total_balance = fields.Float(string="Solde total", compute='_compute_total_balance')

    @api.depends('accounts')
    def _compute_total_balance(self):
        for record in self:
            record.total_balance = sum(record.accounts_ids.mapped("balance"))
