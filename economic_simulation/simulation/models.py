from django.db import models

class Simulation(models.Model):
   
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    policies = models.JSONField(blank=True, null=True)  # Stores simulation policies
    # ... other relevant simulation data fields (e.g., initial economic conditions)

    def __str__(self):
        return f"Simulation ID: {self.id}"

class Character(models.Model):
    period = models.IntegerField()
    name = models.CharField(max_length=50)
    income = models.IntegerField()
    savings = models.IntegerField()
    debt = models.IntegerField()
    happiness = models.IntegerField()
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)  # Foreign key to Simulation

    def __str__(self):
        return f"{self.name} (Simulation: {self.simulation.id})"
        