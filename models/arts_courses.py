from odoo import fields,models,api

class ArtsCourses(models.Model):
    _name="arts.courses"
    _description="Course list for all department"
    _rec_name="course_name"

    course_name=fields.Char(string="Course Name")
    credit_hour = fields.Integer(string="Credit Hour")
    credit_hour_fee=fields.Monetary(string="Hour Fee")
    lab_fee=fields.Monetary(string="Lab Fee")
    single_course_fee=fields.Monetary(string='Subtotal', default=0, compute="_single_course_cost")

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
   