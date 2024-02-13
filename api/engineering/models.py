from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Account(models.Model):
    account_id = models.CharField(primary_key=True, max_length=20)
    account_name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.account_id:
            last_account = Account.objects.order_by('account_id').last()
            if last_account:
                last_id = int(last_account.account_id)
                self.account_id = str(last_id + 1)
            else:
                self.account_id = '1'
        super(Account, self).save(*args, **kwargs)

class Project(models.Model):
    project_id = models.CharField(primary_key=True,max_length=20)
    account_id = models.ForeignKey(Account,on_delete = models.CASCADE)
    project_name = models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        if not self.project_id:
            last_project = Project.objects.order_by('project_id').last()
            if last_project:
                last_id = int(last_project.project_id)
                self.project_id = str(last_id + 1)
            else:
                self.project_id = '1'
        super(Project, self).save(*args, **kwargs)
class User_Project_Mapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Project_id = models.ForeignKey(Project, on_delete=models.CASCADE)