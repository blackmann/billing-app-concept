from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals


Item_Cat = (
    ('RLT', 'registered letter'),
    ('OLT', 'ordinary letter'),
    ('RIT', 'registered item'),
    ('PAR', 'parcel'),
    ('EMS', 'EMS'),
)


class DestRegion(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class DestOffice(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return "%s, %s" % (self.title, self.region.title)


class Region(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class PostOffice(models.Model):
    title = models.CharField(max_length=30)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="postoffices")

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return "%s, %s" % (self.title, self.region.title)


class InOutbound(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class MailDespatch(models.Model):
    region = models.ForeignKey(
        Region, related_name="despatches", on_delete=models.SET_NULL, null=True)
    postoffice = models.ForeignKey(
        PostOffice, related_name="officedespatches", on_delete=models.SET_NULL, null=True)
    op_bal = models.IntegerField()
    item_category = models.CharField(max_length=3, choices=Item_Cat)
    date_sent = models.DateField(auto_now_add=True)
    qty_sent = models.IntegerField()
    dest_region = models.ForeignKey(
        DestRegion, related_name="destinations", on_delete=models.SET_NULL, null=True)
    dest_office = models.ForeignKey(
        DestOffice, related_name="maildestinations", on_delete=models.SET_NULL, null=True)
    date_received = models.DateField(auto_now_add=True)
    qty_received = models.IntegerField()
    qty_delivered = models.IntegerField()
    cls_bal = models.IntegerField()
    comment = models.TextField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    received_by = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on', )


class Transmission(models.Model):
    item_id = models.CharField(max_length=15, null=False)
    item_category = models.CharField(max_length=3, choices=Item_Cat)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="source_region")
    postoffice = models.ForeignKey(
        PostOffice, on_delete=models.CASCADE, related_name="source_office")
    sent_date = models.DateField(auto_now_add=True)
    dest_region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="dest_region")
    dest_postoffice = models.ForeignKey(
        PostOffice, on_delete=models.CASCADE, related_name="dest_office")
    standard_days = models.IntegerField()
    received_date = models.DateField(null=True, blank=True)
    days = models.PositiveIntegerField(default=0)
    day_difference = models.IntegerField(
        default=0, help_text="This is automatically calculated when the \
            received date is set")
    comment = models.TextField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    received_by = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_on', )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.received_date:
            self.set_day_difference()

        return super(Transmission, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def set_day_difference(self):
        diff = self.received_date - self.sent_date
        self.day_difference = diff.days
