from django.db import models
from django.db.models.signals import pre_save

from students.models import Student

# Further fields will be added to reflect more details pertaining to the transaction
# This is the model that will be used to store details from daraja
# Accessed by either by the admin during billing or by the student during payment

class Transaction(models.Model):
    student 	= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount		= models.DecimalField(default=0.0, max_digits=10, decimal_places=0)
    t_type 		= models.CharField(max_length=10, choices=(('D', 'Debit'), ('C', 'Credit')))
    timestamp 	= models.DateTimeField(auto_now_add=True)
    api         = models.BooleanField(default=True)

    def __str__(self, *args, **kwargs):
        return self.student.username

def transaction_pre_save_receiver(sender, instance, *args, **kwargs):
    print(dir(instance.student))
    stud = Student.objects.get(username=instance.student.username)
    print(dir(stud))
    fee = stud.fee_balance
    print(fee)
    if instance.api:
        if instance.t_type == 'D':
            fee += instance.amount
            # print(fee)
        elif instance.t_type == 'C':
            fee -= instance.amount
            # print(fee)
        stud.fee_balance = fee
        print(fee)
        stud.save()

pre_save.connect(transaction_pre_save_receiver, sender=Transaction)
