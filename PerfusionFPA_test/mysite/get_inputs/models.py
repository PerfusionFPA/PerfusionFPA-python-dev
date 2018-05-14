from django.db import models

class GetInputs(models.Model):
    #IDENTIFYING INFO
    patient = models.CharField(max_length=140)
    date = models.DateTimeField()
    #RAW IMAGE INFO (DIRECTLY FROM SCANNER)
    vol1_dcm_path = models.CharField(max_length=500)
    vol2_dcm_path = models.CharField(max_length=500)
    #PROCESSED IMAGE INFO (PROCESSED AFTER SCANNING)
    vol_seg_dcm_path = models.CharField(max_length=500)
    

    def __str__(self):
        return self.patient
