from odoo import fields,models,api

class BusinessFaculty(models.Model):
    _name="business.faculty"
    _description="Business Faculty all department list"

    _rec_name="department_name"
    
    department_name=fields.Char(string="Department Name")
    available_seats=fields.Integer(string="Available Seat", default=20)
    
    hsc_min_grade=fields.Char(string="HSC Grade Required", default="3.50")
    ssc_min_grade=fields.Char(string="SSC Grade Required", default="3.00")
    
    
    hsc_english_min_grade=fields.Char(string="HSC English Grade")
    hsc_finance_min_grade=fields.Char(string="HSC Finance Grade")
    hsc_accounting_min_grade=fields.Char(string="HSC Accounting Grade")

    ssc_english_min_grade=fields.Char(string="SSC English Grade")
    ssc_finance_min_grade=fields.Char(string="SSC Finance Grade")
    ssc_accounting_min_grade=fields.Char(string="SSC Accounting Grade")

    #many2one field with student model
    business_student_id=fields.Many2one('student.registration', string="Student Id")

    