from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string="Price")
    status = fields.Selection(string='Status', selection=[('accepted', "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, readonly=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline', store=True, readonly=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    # --------- Action Buttons ---------#

    def action_accept(self):
        for _offer in self:

            if _offer.property_id.state == "offer_accepted":
                raise UserError("There is already an accepted offer")

            if _offer.property_id.state == "cancelled":
                raise UserError("The Property sale have been canceled")

            # Chercher les autres offres sur la meme propriété et modifier
            property_offers = _offer.property_id.mapped("offer_ids")
            for offer in property_offers:
                offer.status = 'refused'

            _offer.status = 'accepted'
            _offer.property_id.buyer_id = _offer.partner_id.id
            _offer.property_id.selling_price = _offer.price

        return True

    def action_refuse(self):
        for _offer in self:
            _offer.status = 'refused'
            _offer.property_id.buyer_id = ""
            _offer.property_id.selling_price = 0

        return True

    # --------- Constraints ---------#
    _sql_constraints = [
        ("price", "check(price>0)", "Offer Price must me positive"),
        ("validity", "check(validity>0)", "Validity must me positive"),
    ]

