from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError

# Create your models here.
#main project table


class Project(models.Model):
    id = models.AutoField(primary_key = True)
    name =  models.CharField(max_length=100)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    tag_line = models.CharField(max_length=100,default="")
    photo = models.ImageField(upload_to='project/images/')
    year = models.IntegerField()
    sem = models.CharField(max_length=100,default="")
    batch = models.CharField(max_length=100,default="")
    domain = models.CharField(max_length=100)
    guide = models.CharField(max_length=100)
    inspiration = models.TextField(max_length=5000)
    what_it_does = models.TextField(max_length=5000)
    how_we_build = models.TextField(max_length=5000)
    challenges = models.TextField(max_length=5000)
    accomplishment = models.TextField(max_length=5000)
    we_learned = models.TextField(max_length=5000)
    whats_next = models.TextField(max_length=1000)
    verified = models.BooleanField(default=False)
    github = models.URLField(blank=True, max_length=200,null = True)
    hosted = models.URLField(blank=True, max_length=200, null=True)

    def __str__(self):
        # self.slug =
        s = self.name
        li = s.split(" ")
        s = '-'.join(li)
        self.slug = s
        print(self.slug)
        return self.name

admin.site.register(Project)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=16)
    photo = models.ImageField(upload_to='student/images',null = True,default="../media/profile1.jpg")
    github = models.URLField(blank=True, max_length=200,null = True)
    linked_in = models.URLField(blank= True, max_length=200,null = True)
    verified = models.BooleanField(default=False)
    otp = models.IntegerField(null = True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

admin.site.register(Student)

class Guide(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True, default="")
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=16)
    photo = models.ImageField(upload_to='student/images', null=True, default="../media/profile1.jpg")
    # github = models.URLField(blank=True, max_length=200, null=True)
    # linked_in = models.URLField(blank=True, max_length=200, null=True)
    verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    github = models.URLField(blank=True, max_length=200, null=True)
    linked_in = models.URLField(blank=True, max_length=200, null=True)

    def __str__(self):
        return self.name

admin.site.register(Guide)

class Technology(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50)

admin.site.register(Technology)

class Project_Technology(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    tech_label = models.ForeignKey(Technology, on_delete=models.CASCADE)

admin.site.register(Project_Technology)

class Project_Student(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

admin.site.register(Project_Student)

class Project_Guide(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    guide_id = models.ForeignKey(Guide, on_delete=models.CASCADE)
    accept = models.BooleanField(default=False)

admin.site.register(Project_Guide)

class Project_Student_notifications(models.Model):
    student_id =models.ForeignKey(Student, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)

admin.site.register(Project_Student_notifications)

class Project_Guide_notification(models.Model):
    guide_id = models.ForeignKey(Guide, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)

admin.site.register(Project_Guide_notification)


class Images(models.Model):
    photo = models.ImageField(upload_to='tmp/images',null = True)



admin.site.register(Images)


