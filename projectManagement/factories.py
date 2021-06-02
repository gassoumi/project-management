import factory
from .models import Project, UserProject, Discussion
from django.contrib.auth.models import User
from Lib import random


class DiscussionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discussion

    object = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    user = User.objects.get(username="achref")


# factory for the model project
class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    designation = factory.Faker('sentence', nb_words=3)
    objective = factory.Faker('text')
    code = factory.Faker('date_time')


classifications = [
    'Scrum Master',
    'Product Owner',
    'Team Leader',
    'Responsible Development',
    'Responsible',
    'Conception',
    'Executive Assistant',
]


# factory for generate fake data for the model USerProject
class ProjectUsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProject

    user = User.objects.get(username="achref")
    project = factory.SubFactory(ProjectFactory)
    classification = random.choice(classifications)

# factory for create user with a project
# see https://factoryboy.readthedocs.io/en/latest/recipes.html
# class ProjectWithUserFactory(UserFactory):
#     projectUser = factory.RelatedFactory(
#         ProjectUsersFactory,
#         factory_related_name='user',
#     )
