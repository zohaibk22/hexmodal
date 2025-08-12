from django.db import models

# Create your models here.
class PayloadModel(models.Model):
    VALID_STATUS_CHOICES = [
        ('passing', 'Passing'),
        ('failing', 'Failing'),
        ('unknown', 'Unknown'),
    ]
    fCnt = models.IntegerField()
    device = models.ForeignKey('DeviceModel', on_delete=models.CASCADE, related_name='payloads')
    data_b64 = models.CharField(max_length=4096)
    data_hex = models.CharField(max_length=8192)
    status = models.CharField(max_length=20, choices=VALID_STATUS_CHOICES, default='unknown')
    rx_info = models.JSONField(null=True, blank=True)
    tx_info = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['device','fCnt'],
            name = 'uniq_device_fCnt')
        ]


class DeviceModel(models.Model):

    VALID_STATUS_CHOICES = [
        ('passing', 'Passing'),
        ('failing', 'Failing'),
        ('unknown', 'Unknown'),
    ]
    device_eui = models.CharField(max_length=50, unique=True)
    latest_status = models.CharField(max_length=20, choices=VALID_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Device {self.device_eui} - Status: {self.status}"


