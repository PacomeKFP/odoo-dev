from odoo import fields, models, api

class CustomerPartner(models.Model):
    # _name = "knance.customer"
    _inherit = 'res.partner'
    _description = 'The customer'

    account_ids = fields.One2many("knance.account", "customer_id", string="Vos comptes")

    total_balance = fields.Float(string="Solde total", compute='_compute_total_balance')
    street = fields.Char(string='Adresse')

    @api.depends('account_ids.balance')
    def _compute_total_balance(self):
        for record in self:
            record.total_balance = sum(record.account_ids.mapped("balance"))

    @api.model
    def create(self, vals_list):
        print("startup")
        # index = '{:0>6}'.format(self.env["knance.account"].search_count(domain=[]) + 1)
        index = '{:0>6}'.format(1)
        print("before")
        created_customer = super().create(vals_list)
        print("after")
        self.env["knance.account"].create({
            "number": f"AC-{index}",
            "customer_id": created_customer.id,
        })
        print('end')

        return created_customer