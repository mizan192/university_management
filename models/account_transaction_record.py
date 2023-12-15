from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class StudentAccount(models.Model):
    _name="account.transaction.record"
    _description="Students account transaction recored"

    s_name=fields.Char(string='Name')
    s_id = fields.Char(string='Student ID')
    amount_paid=fields.Monetary(string='Amcount', currency_field='currency_id')
    payment_date=fields.Date(string='Payment Date', default=fields.Date.today)
    transaction_id=fields.Char(string='Transaction ID')
    record_id=fields.Char(string='Record ID')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
       

