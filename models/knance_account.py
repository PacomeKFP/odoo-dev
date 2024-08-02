from odoo import fields, models, api


class Account(models.Model):
    _name = 'knance.account'
    _description = 'Account'

    name = fields.Char(string="Libelé", default="Principal")
    number = fields.Char(string="Numero de compte ", default="0")

    customer_id = fields.Many2one('res.partner', string="Proprietaire")

    transaction_ids = fields.One2many('knance.transaction', 'account_id', string="Transactions")

    balance = fields.Float(string="Solde", compute='_compute_balance')

    @api.depends('transaction_ids')
    def _compute_balance(self):
        for account in self:
            account.balance = 0
            for transaction in account.transaction_ids:
                transaction.balance += account.relative_amount



