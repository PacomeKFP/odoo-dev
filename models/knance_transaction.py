from odoo import fields, models, api, _
from odoo.exceptions import UserError
from random import randint


class Transaction(models.Model):
    _name = 'knance.transaction'
    _description = 'Transaction'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # --------- Transaction data ---------#
    # la reference de la transaction
    name = fields.Char("Reference de la Transaction", default="Nouveau", readonly=True, store=True)

    # le type de transaction
    transaction_type = fields.Selection(
        string="Type de transaction",
        selection=[("deposit", "Dépot"), ("withdrawal", "Retrait")],
        default="deposit")

    # le status de la transaction
    state = fields.Selection(
        string="Etat",
        selection=[
            ("pending", "En attente"),
            ("done", "Réalisée"),
            ("canceled", "Annulée")],
        default='pending'
    )

    # le montant de la transaction
    amount = fields.Float(string="Montant de la transaction", required=True)

    # le montant relatif de la transaction (positif ou negatif en fonction du type de transaction)
    relative_amount = fields.Float(string="Montant relatif", compute="_compute_relative_amount")

    # Le client dont le compte va être affecté par la transaction
    customer_id = fields.Many2one(comodel_name='knance.customer', string="Client", readonly=True)

    # Le collecteur qui initie la transaction
    collector_id = fields.Many2one(comodel_name='knance.collector', string="Collecteur", readonly=False)

    active = fields.Boolean(string="Activé", default=True)

    # TODO: rajouter le solde avant et apres transaction

    # --------- Contraintes ---------#
    _sql_constraints = [
        ("positive_amount", "CHECK(amount > 0)", "Le montant de la transaction doit être strictement positif"),
    ]

    # --------- CONSTRAINTS ---------#
    @api.constrains("transaction_type", "amount", "customer_id")
    def _ensure_withdrawal_possibility(self):
        for transaction in self:
            # En cas de retrait s'assurer que le montant à retirer inférieur au solde
            if (transaction.transaction_type == "withdrawal"
                    and transaction.customer_id.account_balance <= transaction.amount):
                raise UserError("Retrait impossible - Le montant demandé est supérieur au solde du compte")

    # --------- CRUDs ---------#
    @api.model_create_multi
    def create(self, vals_list):
        transactions = super(Transaction, self).create(vals_list)
        for transaction in transactions:
            if transaction.name == _("Nouveau"):
                transaction.name = self.env['ir.sequence'].next_by_code('knance.transaction.seq') or _(
                    'Nouveau')
        return transactions

    # --------- Computations for fields ---------#
    @api.depends("amount", "transaction_type")
    def _compute_relative_amount(self):
        for transaction in self:
            transaction.relative_amount = transaction.amount if transaction.transaction_type == "deposit" else -transaction.amount
