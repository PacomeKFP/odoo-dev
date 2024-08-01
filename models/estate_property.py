from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):

        def _compute_invoice_price(_property):
            return 1.06 * _property.selling_price + 100

        for _property in self:
            if super().action_sold():
                move_data = {
                    "move_type": "out_invoice",
                    "partner_id": _property.buyer_id.id,
                    "invoice_line_ids": [
                        fields.Command.create(
                            {
                                "name": f"Commission and fees on sold of <b>{_property.name}</b>",
                                "quantity": 1,
                                "price_unit": _compute_invoice_price(_property),
                            }
                        ),
                        fields.Command.create(
                            {
                                "name": _property.name,
                                "quantity": 1,
                                "price_unit": _property.selling_price,
                            }
                        )
                    ]
                }

                self.env['account.move'].create(move_data)

        return True
