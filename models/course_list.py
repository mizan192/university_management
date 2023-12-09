from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError


class CourseList(models.Model):
    _name="course.list"
    _description="Course list for all department"
    _rec_name="course_name"

    course_name=fields.Char(string="Course Code")
    course_faculty= fields.Selection([('all','All Faculty'),('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], default='all', string='Course Faculty')
    credit_hour=fields.Float(string="Credit Hour", default=2)
    credit_hour_fee=fields.Float(string="Hour Fee", default=2000)
    lab_fee=fields.Float(string="Lab Fee")
    single_course_fee=fields.Float(string='Subtotal', default=0, compute="_single_course_cost", store=True)


    # course selection 
    students_id=fields.Many2one(
        comodel_name='student.registration',
        # string="Students list"  
    )


    # calculate single course cost depending on credit_hour,credit_hour_fee,lab_fee
    @api.depends('credit_hour','credit_hour_fee','lab_fee')
    def _single_course_cost(self):
        self.single_course_fee=0
        for rec in self:
            rec.single_course_fee=rec.credit_hour*rec.credit_hour_fee




    # duplicate record check 
    @api.constrains('course_name')
    def _check_duplicate_name(self):
        for record in self:
            if record.search_count([('course_name', 'ilike', record.course_name)]) > 1:
                raise ValidationError("Duplicate record with the same name found!")


# add course to faculty course list : not usese after logic chnage 
    @api.model
    def course_add_in_faculty(self,course_faculty,course_name,credit_hour,credit_hour_fee,lab_fee,single_course_fee):
        if course_faculty=='engineering' or course_faculty=='all':
            self.env['engineering.courses'].create({
                'course_name':course_name,
                'credit_hour':credit_hour,
                'credit_hour_fee':credit_hour_fee,
                'lab_fee':lab_fee,
                'single_course_fee':single_course_fee,
            })
        if course_faculty=='business' or course_faculty=='all':
            self.env['business.courses'].create({
                'course_name':course_name,
                'credit_hour':credit_hour,
                'credit_hour_fee':credit_hour_fee,
                'lab_fee':lab_fee,
                'single_course_fee':single_course_fee,
            })
        if course_faculty=='arts' or course_faculty=='all':
            self.env['arts.courses'].create({
                'course_name':course_name,
                'credit_hour':credit_hour,
                'credit_hour_fee':credit_hour_fee,
                'lab_fee':lab_fee,
                'single_course_fee':single_course_fee,
            })
        


    @api.model
    def create(self,val):
        ctx = self.env.context.copy()
        rec=super(CourseList,self.with_context(ctx)).create(val)
        self.course_add_in_faculty(rec.course_faculty,rec.course_name,rec.credit_hour,rec.credit_hour_fee,rec.lab_fee,rec.single_course_fee)
        return rec