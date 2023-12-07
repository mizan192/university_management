from odoo import fields,models,api

class EngineeringFaculty(models.Model):
    _name="engineering.faculty"
    _description="Engineering Faculty all department list"

    _rec_name="department_name"

    department_name=fields.Char(string="Department Name")
    available_seats=fields.Integer(string="Available Seat", default=20)
    
    hsc_min_grade=fields.Char(string="HSC Grade Required", default="3.50")
    ssc_min_grade=fields.Char(string="SSC Grade Required", default="3.00")
    
    
    hsc_math_min_grade=fields.Char(string="HSC Math Grade")
    hsc_physics_min_grade=fields.Char(string="HSC physics Grade")
    hsc_chemisty_min_grade=fields.Char(string="HSC chemisty Grade")
    hsc_biology_min_grade=fields.Char(string="HSC Biology Grade")
    hsc_english_min_grade=fields.Char(string="HSC English Grade")

    ssc_math_min_grade=fields.Char(string="SSC Math Grade")
    ssc_physics_min_grade=fields.Char(string="SSC physics Grade")
    ssc_chemisty_min_grade=fields.Char(string="SSC chemisty Grade")
    ssc_biology_min_grade=fields.Char(string="SSC Biology Grade")
    ssc_english_min_grade=fields.Char(string="SSC English Grade")


    #many2one field with student model
    eng_student_id=fields.Many2one('student.registration', string="Student Id")

