from odoo import fields,models,api

class ArtsFaculty(models.Model):
    _name="arts.faculty"
    _description="Arts Faculty all department list"

    _rec_name="department_name"

    
    department_name=fields.Char(string="Department Name")
    available_seats=fields.Integer(string="Available Seat", default=20)
    
    hsc_min_grade=fields.Char(string="HSC Grade Required", default="3.50")
    ssc_min_grade=fields.Char(string="SSC Grade Required", default="3.00")
    
    
    hsc_english_min_grade=fields.Char(string="HSC English Grade")
    ssc_english_min_grade=fields.Char(string="SSC English Grade")
    
    #many2one field with student model
    arts_student_id=fields.Many2one('student.registration', string="Student Id")

    