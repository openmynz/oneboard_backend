from django.db import models


class LdapUsers(models.Model):
    """Model to store LDAP user details."""

    distinguished_name = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    common_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=100,db_index=True)


class Employee(models.Model):
    """Model to capture employee information."""

    # Define blood group choices
    BLOOD_GROUPS = (
        ("O+", "O+"),
        ("O-", "O-"),
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
    )

    # Define role choices
    ROLE_CHOICES = (
        ("Manager", "Manager"),
        ("Employee", "Employee"),
        ("Supervisor", "Supervisor"),
        # Add more roles as necessary
    )

    employee_id = models.PositiveBigIntegerField(unique=True, db_index=True)
    joining_date = models.DateField()
    ldap_user = models.OneToOneField(
        "LdapUsers", on_delete=models.CASCADE, related_name="ldap_user"
    )
    reports_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )
    contact_number = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    email_id = models.CharField(unique=True, max_length=100, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    blood_group = models.CharField(max_length=3, blank=True, choices=BLOOD_GROUPS)
    profile_photo = models.ImageField(
        upload_to="profile_photos/", null=True, blank=True
    )

    def __str__(self):
        return f"{self.employee_id} - {self.email_id}"
