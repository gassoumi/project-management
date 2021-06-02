from django.db import models
from .apps import ProjectmanagementConfig
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


# models representing database of the current app

class Discussion(models.Model):
    user = models.ForeignKey(User, related_name="discussions", on_delete=models.CASCADE)
    object = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.object


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(default=now)

    # - reverse order
    class Meta:
        ordering = ['-modified_at']

    def __str__(self):
        return self.description


class Note(models.Model):
    note = models.CharField(max_length=300)
    ok = models.BooleanField(default=True)
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.note


class Project(models.Model):
    code = models.CharField(max_length=200, unique=True)
    designation = models.CharField(max_length=200, unique=True)
    objective = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, through='UserProject')

    class Meta:
        ordering = ['designation']

    def __str__(self):
        return self.designation


class UserProject(models.Model):
    class Classification(models.TextChoices):
        SCRUM_MASTER = 'Scrum Master', _('Scrum Master')
        PRODUCT_OWNER = 'Product Owner', _('Product Owner')
        TEAM_OWNER = 'Team Leader', _('Team Leader')
        RESPONSIBLE_DEVELOPMENT = 'Responsible Development', _('Responsible Development')
        RESPONSIBLE = 'Responsible', _('Responsible')
        CONCEPTION = 'Conception', _('Conception')
        EXECUTIVE_ASSISTANT = 'Executive Assistant', _('Executive Assistant')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="projectUsers", on_delete=models.CASCADE)
    classification = models.CharField(choices=Classification.choices, max_length=50)

    def is_scrum_master(self):
        return self.classification == self.Classification.SCRUM_MASTER

    is_scrum_master.boolean = True
    is_scrum_master.short_description = 'Is Scrum master?'
    is_scrum_master.admin_order_field = 'classification'

    def __str__(self):
        return '%s- %s' % (self.project.designation, self.user.username)

    class Meta:
        db_table = ProjectmanagementConfig.name + "_user_project"
        unique_together = (("user", "project"),)


class Video(models.Model):
    # TODO remove the default param later
    docFile = models.FileField(upload_to='videos/%Y/%m/%d', default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.docFile.name


class Sprint(models.Model):
    class Status(models.TextChoices):
        PLANIFIE = 'Planifiè', _('Planifiè')
        EN_COURS = 'En Cours', _('En Cours')
        CLOTURE = 'Cloturé', _('Cloturé')
        ARCHIVE = 'Archivé', _('Archivé')

    name = models.CharField(max_length=500, unique=True)
    desired_at = models.DateTimeField()
    project = models.ForeignKey(Project, related_name="sprints", on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        BACKLOG = 'Backlog', _('Backlog')
        A_FAIRE = 'A Faire', _('A Faire')
        EN_COURS = 'En Cours', _('En Cours')
        A_VERIFIER = 'A Verifier', _('A Verifier')
        TERMINEE = 'Termine', _('Termine')

    description = models.CharField(max_length=200, unique=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, blank=True)
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, max_length=50)

    def __str__(self):
        return self.description


class Problem(models.Model):
    class Status(models.TextChoices):
        CLOTURE = 'CLOTURE', _('cloturé')
        NON_CLOTURE = 'NON_CLOTURE', _('non cloturé')

    description = models.TextField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    cause = models.TextField()
    task = models.ForeignKey(Task, related_name="problems", on_delete=models.CASCADE)
    resolutionTools = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=now)
    status = models.CharField(choices=Status.choices, max_length=50, default=Status.NON_CLOTURE)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-created_at']


# https://docs.djangoproject.com/en/3.0/topics/files/#file-storage
# https://docs.djangoproject.com/en/3.0/howto/static-files/#serving-uploaded-files-in-development
# https://docs.djangoproject.com/en/3.0/topics/files/
# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://docs.djangoproject.com/en/3.0/ref/forms/api/#binding-uploaded-files
# https://stackoverflow.com/questions/5871730/how-to-upload-a-file-in-django
class Document(models.Model):
    # Actuel  et Périmé
    class Status(models.TextChoices):
        ACTUAL = 'AC', _('Actuel')
        EXPIRED = 'EX', _('Périmé')

    code = models.CharField(max_length=200, unique=True)
    version = models.CharField(max_length=20)
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    task = models.ForeignKey(Task, related_name="documents", on_delete=models.SET_NULL, null=True, blank=True,
                             default=None)
    # task = models.ForeignKey(Task, related_name="documents", on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    docFile = models.FileField(upload_to='documents/%Y/%m/%d')
    status = models.CharField(choices=Status.choices, max_length=2, default=Status.ACTUAL)

    class Meta:
        ordering = ['created_at']

    def get_doc_file_name(self):
        return self.docFile.name

    def get_doc_file_path(self):
        return self.docFile.path

    def __str__(self):
        return self.docFile.name
