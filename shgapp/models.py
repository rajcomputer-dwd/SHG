from django.db import models

class BranchDetails(models.Model):
    branchcode = models.BigIntegerField()
    branchname = models.CharField(max_length=255)
    br_manager = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    taluka = models.CharField(max_length=255)
    district = models.CharField(max_length=255)

    def __str__(self):
        return self.branchname

class SocietyDetails(models.Model):
    society_code = models.BigIntegerField()
    society_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    taluka = models.CharField(max_length=255)
    district = models.CharField(max_length=255)

    def __str__(self):
        return self.society_name


class shgdetails(models.Model):
    type = models.CharField(max_length=255)
    ac_open_through = models.CharField(max_length=255)
    sycode = models.BigIntegerField()
    society_name = models.CharField(max_length=255)
    branchname = models.CharField(max_length=255)
    taluka = models.CharField(max_length=255)
    group_no = models.BigIntegerField()
    group_name = models.CharField(max_length=1000)
    date = models.DateField()
    group_type = models.CharField(max_length=255)
    No_of_members = models.BigIntegerField()
    of_which_sc = models.BigIntegerField()
    of_which_st = models.BigIntegerField()
    total_savings = models.BigIntegerField()
    balance = models.BigIntegerField()

class shgtransaction(models.Model):
    sycode = models.BigIntegerField()
    society_name = models.CharField(max_length=255)
    branchname = models.CharField(max_length=255) 
    taluka = models.CharField(max_length=255)
    group_no = models.BigIntegerField()
    group_name = models.CharField(max_length=1000)
    date_of_advance = models.DateField()
    loan_amt = models.BigIntegerField()
    opeaning_outstanding_amt = models.BigIntegerField()
    recovery_period_from = models.DateField()
    recovery_period_to = models.DateField()
    recovery_date = models.DateField()
    no_of_days = models.BigIntegerField()
    new_outstanding_amt = models.BigIntegerField()
    principal_received = models.BigIntegerField()
    interest_received = models.FloatField()
    interest1 = models.FloatField()
    intreset2 = models.FloatField()










