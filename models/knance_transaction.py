from odoo import fields, models, api


class Transaction(models.Model):
    _name = 'knance.transaction'
    _description = 'Transaction'

    transaction_type = fields.Selection(
        string="Type de transaction",
        selection=[("deposit", "Dépot"), ("withdrawal", "Retrait")],
        default="deposit")

    amount = fields.Float(string="Amount")
    relative_amount = fields.Float(string="Relative amount", compute="_compute_relative_amount")

    account_id = fields.Many2one('knance.account', string="Account")

    _sql_constraints = [
        ("amount", "check(amount>0)", "Le montant de la transaction doit  strictement positif"),
    ]

    @api.depends("amount")
    def _compute_relative_amount(self):
        for transaction in self:
            if transaction.transaction_type == "deposit":
                transaction.relative_amount = transaction.amount
            else:
                transaction.relative_amount = -1 * transaction.amount
