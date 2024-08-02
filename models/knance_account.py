from odoo import fields, models, api


class Account(models.Model):
    _name = 'knance.account'
    _description = 'Account'

    name = fields.Char(string="Libelé", default="Principal")
    number = fields.Char(string="Numéro de compte", default="0")

    customer_id = fields.Many2one('res.partner', string="Propriétaire")

    transaction_ids = fields.One2many('knance.transaction', 'account_id', string="Transactions")

    balance = fields.Float(string="Solde", compute='_compute_balance', store=True)

    @api.depends('transaction_ids.relative_amount')
    def _compute_balance(self):
        for account in self:
            account.balance = sum(account.transaction_ids.mapped('relative_amount'))


