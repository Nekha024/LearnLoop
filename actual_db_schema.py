# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    role = models.CharField(max_length=10)
    phone_number = models.CharField(unique=True, max_length=10, blank=True, null=True)
    previous_experience = models.BooleanField(blank=True, null=True)
    is_approved = models.BooleanField()
    available_days = models.JSONField()
    available_from = models.TimeField()
    available_to = models.TimeField()
    bio = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    expertise = models.CharField(max_length=100, blank=True, null=True)
    intro_video = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    portfolio = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.CharField(max_length=100, blank=True, null=True)
    session_duration = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'accounts_customuser'


class AccountsCustomuserGroups(models.Model):
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_groups'
        unique_together = (('customuser', 'group'),)


class AccountsCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MentorAppointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    mentor = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING, related_name='mentorappointment_user_set')

    class Meta:
        managed = False
        db_table = 'mentor_appointment'


class MentorsAppointment(models.Model):
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    mentor = models.ForeignKey('MentorsMentorprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mentors_appointment'


class MentorsBlogarticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField()
    mentor = models.ForeignKey('MentorsMentorprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mentors_blogarticle'


class MentorsEnquiry(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField()
    is_responded = models.BooleanField()
    user = models.ForeignKey(AccountsCustomuser, models.DO_NOTHING)
    mentor = models.ForeignKey('MentorsMentorprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mentors_enquiry'


class MentorsMentorprofile(models.Model):
    bio = models.TextField()
    expertise = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    profile_image = models.CharField(max_length=100, blank=True, null=True)
    available_days = models.CharField(max_length=255)
    available_time_from = models.TimeField(blank=True, null=True)
    available_time_to = models.TimeField(blank=True, null=True)
    user = models.OneToOneField(AccountsCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mentors_mentorprofile'
