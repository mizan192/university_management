from odoo import fields,models,api

class CourseList(models.Model):
    _name="course.list"
    _description="Course list for all department"
    _rec_name="course_name"

    course_name=fields.Char(string="Course Name")
    course_faculty= fields.Selection([('all','All Department'),('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], default='all', string='Course Faculty')
    credit_hour = fields.Integer(string="Credit Hour", default=10)
    credit_unit=fields.Float(string="Credit Unit", default=2)
    credit_hour_fee=fields.Integer(string="Hour Fee", default=2000)
    lab_fee=fields.Integer(string="Lab Fee")






    @api.model
    def course_add_in_faculty(self,course_faculty,course_name,credit_hour,credit_unit,credit_hour_fee,lab_fee):
        if course_faculty=='engineering' or course_faculty=='all':
            self.env['engineering.courses'].create({
                'course_name':course_name,
                'credit_hour':credit_hour,
                'credit_unit':credit_unit,
                'credit_hour_fee':credit_hour_fee,
                'lab_fee':lab_fee,
            })
        if course_faculty=='business' or course_faculty=='all':
            self.env['business.courses'].create({
                'course_name':course_name,
                'credit_hour':credit_hour,
                'credit_unit':credit_unit,
                'credit_hour_fee':credit_hour_fee,
                'lab_fee':lab_fee,
            })
        if course_faculty=='arts' or course_faculty=='all':
            self.env['arts.courses'].create({
                'course_name':course_name,
                'credit_hour':credit_hour,
                'credit_unit':credit_unit,
                'credit_hour_fee':credit_hour_fee,
                'lab_fee':lab_fee,
            })
        


    @api.model
    def create(self,val):
        ctx = self.env.context.copy()
        rec=super(CourseList,self.with_context(ctx)).create(val)
        self.course_add_in_faculty(rec.course_faculty,rec.course_name,rec.credit_hour,rec.credit_unit,rec.credit_hour_fee,rec.lab_fee)
        return rec