from django.db import models
from django.contrib.auth.models import User


class ClientType(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Country(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class City(models.Model):
    title = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return "%s, %s" % (self.title, self.country.title)


class Zone(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Client(models.Model):
    title = models.CharField(max_length=100)
    client_type = models.ForeignKey(ClientType, on_delete=models.SET_NULL, null=True, related_name="clients")
    city = models.ForeignKey(City, related_name="clients", on_delete=models.SET_NULL, null=True)
    standard_weight = models.DecimalField(decimal_places=2, max_digits=10)
    initial_charge = models.DecimalField(decimal_places=3, max_digits=10)
    additional_charge = models.DecimalField(decimal_places=3, max_digits=10)
    charge_cat = models.CharField(max_length=20)
    multiplier = models.IntegerField()
    group_code = models.CharField(max_length=20)
    contracted_on = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Transaction(models.Model):
    receipt_number = models.CharField(max_length=50)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    client = models.ForeignKey(Client, related_name="transactions", on_delete=models.CASCADE)
    a_weight = models.DecimalField(decimal_places=2, max_digits=10)
    s_weight = models.DecimalField(decimal_places=2, max_digits=10)
    f_index = models.IntegerField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created_on', )
