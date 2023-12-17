from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError
import re

class DepartmentMigration(models.Model):
    _name="department.migration"
    _description="Department switch process"

    name=fields.Char(string='Name', compute='retrive_student_details', store=True)
    student_id=fields.Char(string='Student ID', compute='retrive_student_details', store=True)
    # registration_id=fields.Char(string='Registration Id')
    birth_date=fields.Date(string='Birth Date', compute='retrive_student_details', store=True)
    image=fields.Binary(string='Image', compute='retrive_student_details', store=True)
    age = fields.Integer(string="age", compute='retrive_student_details', store=True)
    email=fields.Char(string='Email', compute='retrive_student_details', store=True)
    contact_number=fields.Char(string='Contact Number', compute='retrive_student_details', store=True)
    admission_date=fields.Date(string='Admission Date', compute='retrive_student_details', store=True)
    previous_faculty=fields.Char(string='Previous Faculty', compute='retrive_student_details', store=True)
    previous_department=fields.Char(string='Previous Department', compute='retrive_student_details', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    due = fields.Monetary(string='Due Amount', compute='retrive_student_details', store=True)

    reg_id = fields.Many2one(
        comodel_name='student.registration',
        domain="[('registration_status','=','Enrolled'),('registration_id', '!=', False)]",
        # placeholder="Student Registration no",
    )



# select switched faculty and department 
 
    # faculty_choice=fields.Selection([('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], default='arts', string='Select Faculty' )

    # engineering_departments=fields.Many2one(
    #     comodel_name='engineering.faculty',
    #     # inverse_name='eng_student_id',
    #     string='Engineering Department'
    # )
    # business_departments=fields.Many2one(
    #     comodel_name='business.faculty',
    #     # inverse_name='business_student_id',
    #     string="Business Department"
    # )
    # arts_departments=fields.Many2one(
    #     comodel_name='arts.faculty',
    #     # inverse_name='arts_student_id',
    #     string="Arts Department"
    # )

    
    # accepted_faculty=fields.Char(string="Faculty", readonly=True)
    # accepted_department=fields.Char(string="Department",readonly=True)
    # congres_group=fields.Char(default="not_confirm")
    # is_admitted=fields.Boolean(default=False)
    # department_obj =fields.Char(string="Object")


    # REG_STATUS_SELECTION = [
    #     ('Draft', 'Draft'),
    #     ('Reviewing', 'Reviewing'),
    #     ('Enrolled', 'Enrolled'),
    # ]

    # registration_status = fields.Selection(
    #     selection=REG_STATUS_SELECTION,
    #     string='Admission Status',
    #     default='Draft',  
    # )
    # course_ids=fields.One2many(
    #     comodel_name='course.list',
    #     inverse_name='students_id',
    #     domain="['|',('course_faculty', '=', 'all'),('course_faculty', '=', accepted_faculty)]",
    #     # string="select course"  
    # )






    @api.onchange('reg_id')
    def show_student_details(self):
        self.name=self.reg_id.name
        self.student_id=self.reg_id.student_id
        self.image=self.reg_id.image
        self.email=self.reg_id.email
        self.admission_date=self.reg_id.admission_date
        self.previous_department=self.reg_id.accepted_department
        self.previous_faculty=self.reg_id.accepted_faculty
        self.due=self.reg_id.total_cost

    @api.depends('reg_id')
    def retrive_student_details(self):
        for rec in self:
            rec.name=rec.reg_id.name
            rec.student_id=rec.reg_id.student_id
            rec.image=rec.reg_id.image
            rec.email=rec.reg_id.email
            rec.admission_date=rec.reg_id.admission_date
            rec.previous_department=rec.reg_id.accepted_department
            rec.previous_faculty=rec.reg_id.accepted_faculty
            rec.due=rec.reg_id.total_cost

    