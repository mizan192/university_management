from odoo import fields,models,api

class BusinessCourses(models.Model):
    _name="business.courses"
    _description="Course list for all department"
    _rec_name="course_name"

    course_name=fields.Char(string="Course Name")
    credit_hour = fields.Integer(string="Credit Hour", default=10)
    credit_hour_fee=fields.Integer(string="Hour Fee", default=2000)
    lab_fee=fields.Integer(string="Lab Fee")
    single_course_fee=fields.Float(string='Subtotal', default=0, compute="_single_course_cost")

