from odoo import fields, models, api


class Transaction(models.Model):
    _name = 'knance.transaction'
    _description = 'Transaction'

    transaction_type = fields.Selection(
        string="Type de transaction",
        selection=[("deposit", "Dépot"), ("withdrawal", "Retrait")],
        default="deposit")

    amount = fields.Float(string="Amount")
    relative_amount = fields.Float(string="Relative amount", compute="_compute_relative_amount", store=True)

    account_id = fields.Many2one('knance.account', string="Account")

    _sql_constraints = [
        ("positive_amount", "CHECK(amount > 0)", "Le montant de la transaction doit être strictement positif"),
    ]

    @api.depends("amount", "transaction_type")
    def _compute_relative_amount(self):
        for transaction in self:
            transaction.relative_amount = transaction.amount if transaction.transaction_type == "deposit" else -transaction.amount