from odoo import fields, models, api, _
from random import randint


class Customer(models.Model):
    _name = 'knance.customer'
    _description = 'le Client'
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.activity.mixin', 'mail.thread']

    # --------- Customer data ---------#
    # Other information about the customer are inherited from the res.partner model
    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the customer')
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)
    phone = fields.Char(related='partner_id.phone', inherited=True, readonly=False)
    street = fields.Char(related='partner_id.street', inherited=True, readonly=False, string='Adresse')
    # --------- Customer Account data ---------#
    account_name = fields.Char(string="Nom du compte", default="Compte Principal", readonly=True)
    account_number = fields.Char(string="Numéro de compte", default="Nouveau", readonly=True)
    account_balance = fields.Float(string="Solde", compute='_compute_balance')

    transaction_ids = fields.One2many('knance.transaction', 'customer_id', string="Transactions", required=True)

    active = fields.Boolean(string="Activé", default=True)

    # --------- CRUDs ---------#
    @api.model_create_multi
    def create(self, data_list):
        records = super().create(data_list)
        for record in records:
            if record.account_number == _('Nouveau'):
                record.account_number = self.env['ir.sequence'].next_by_code('knance.customer.account_number.seq') or _(
                    'Nouveau')
        return records

        # si tout se passe bien, on enregistre le client avec son compte principal

    # --------- Computations for fields ---------#
    @api.depends('transaction_ids.relative_amount')
    def _compute_balance(self):
        for customer in self:
            customer.account_balance = sum(customer.transaction_ids.mapped('relative_amount'))
