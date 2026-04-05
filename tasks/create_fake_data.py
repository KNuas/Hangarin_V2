from faker import Faker
import random
from tasks.models import Task, SubTask, Category, Priority, Note
from django.utils import timezone

fake = Faker()


def run():
   
    Task.objects.all().delete()
    SubTask.objects.all().delete()
    Note.objects.all().delete()
    Category.objects.all().delete()
    Priority.objects.all().delete()

  
    categories = []
    for name in ["Work", "School", "Personal", "Finance", "Projects"]:
        categories.append(Category.objects.create(name=name))

    
    priorities = []
    for name in ["High", "Medium", "Low", "Critical", "Optional"]:
        priorities.append(Priority.objects.create(name=name))

    
    tasks = []
    for _ in range(30):
        task = Task.objects.create(
            title=fake.sentence(nb_words=4),
            description=fake.text(),
            deadline=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
            status=random.choice(["Pending", "In Progress", "Completed"]),
            category=random.choice(categories),
            priority=random.choice(priorities),
        )
        tasks.append(task)

   
    for _ in range(30):
        SubTask.objects.create(
            parent_task=random.choice(tasks),
            title=fake.sentence(nb_words=3),
            status=random.choice(["Pending", "In Progress", "Completed"]),
        )

    
    for _ in range(30):
        Note.objects.create(
            task=random.choice(tasks),
            content=fake.text(),
        )

    print("Fake data created successfully!")