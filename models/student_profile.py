from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class StudentProfile(models.Model):
    _name= 'student.profile'
    _description='Registered Student Profile'
    _rec_name="name"

    name = fields.Char(string="Name")
    student_id=fields.Char(string='Student ID')
    registration_id=fields.Char(string='Registration ID')
    accepted_faculty=fields.Char(string="Faculty", readonly=True)
    accepted_department=fields.Char(string="Department",readonly=True)

    student_relation=fields.Many2one("student.registration")    
    course_cost=fields.Monetary(string="Course Cost")
    hsc_result=fields.Float(string='HSC')
    ssc_result=fields.Float(string='SSC')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    total_fee=fields.Monetary(string='Fee', readonly='1')
