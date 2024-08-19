from odoo import fields, models, api


class CollectorUser(models.Model):
    """
        la classe metier qui represente les collecteurs
    """
    _name = 'knance.collector'
    _description = 'Le Collecteur'

    _inherits = {'hr.employee': "employee_id"}
    _inherit = ['mail.activity.mixin', 'mail.thread']

    employee_id = fields.Many2one(comodel_name='hr.employee', requred=True, ondelete='restrict', auto_join=True,
                                  index=True,
                                  string='Related Employee')
    name = fields.Char(related='employee_id.name', inherited=True, readonly=False)
    email = fields.Char(related='employee_id.private_email', inherited=True, readonly=False)
    phone = fields.Char(related='employee_id.private_phone', inherited=True, readonly=False)
    partner_id = fields.Many2one(related='employee_id.user_partner_id', inherited=True, readonly=False)

    # les transactions qu'il initie
    transaction_ids = fields.One2many(comodel_name="knance.transaction", inverse_name="collector_id",
                                      string="Transactions")
    active = fields.Boolean(string="Activé", default=True)

    # TODO: rajouter des champs pour le total collecté aujourd'hui et dans la semaine
