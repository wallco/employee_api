from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet

#Model representing hired employee entities in the DB
class HiredEmployee(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # ids can't be null
    employee_id = models.IntegerField(null=False, blank=False)
    # It was not specified if the other fields could contain null values, so this may change
    name = models.TextField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    department_id = models.IntegerField(null=True, blank=True)
    job_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.employee_id

#Model representing department entities in the DB  
class Department(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # Ids can't be null
    department_id = models.IntegerField(null=False, blank=False)
    # it was not specified if the other fields could contain null values, so this may change
    department = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.department_id


#Model representing job entities in the DB
class Job(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    # Ids can't be null
    job_id = models.IntegerField(null=False, blank=False)
    # it was not specified if the other fields could contain null values, so this may change
    job= models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.job_id