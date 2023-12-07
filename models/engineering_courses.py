from odoo import fields,models,api

class EngineeringCourses(models.Model):
    _name="engineering.courses"
    _description="Course list for all department"
    _rec_name="course_name"

    course_name=fields.Char(string="Course Name")
    credit_hour = fields.Integer(string="Credit Hour")
    credit_unit=fields.Float(string="Credit Unit")
    credit_hour_fee=fields.Integer(string="Hour Fee")
    lab_fee=fields.Integer(string="Lab Fee")

