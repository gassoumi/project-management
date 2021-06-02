from rest_framework import serializers

from .models import Project, UserProject, Sprint, Task, Document, Comment, Discussion, Note, Problem
from django.contrib.auth.models import User

"""
    user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(write_only=True)
"""


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


# UserProject Serializer
class UserProjectSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    # put it if it is required in json input for creating or updating the UserProjectModel
    # is_responsible = serializers.BooleanField()
    username = serializers.CharField(source='user.username')
    user = serializers.CharField(source='user.id', read_only=True)
    # classification = serializers.ChoiceField(choices=UserProject.Classification)

    # code = serializers.CharField(source='project.code', read_only=True)
    # user = UserSerializer(required=False, read_only=True)
    project = serializers.IntegerField(read_only=True, source="project.id")

    class Meta:
        fields = '__all__'
        # fields = ('id', 'username', 'classification',)
        model = UserProject


# Project serializer
class ProjectSerializer(serializers.ModelSerializer):
    # If the name of the output is different
    # users = UserProjectSerializer(source='projectUsers', many=True)
    projectUsers = UserProjectSerializer(many=True, required=True, )

    class Meta:
        model = Project
        fields = ['id', 'code', 'designation',
                  'objective', 'created_at', 'projectUsers']
        # fields = "__all__"

    # Check at least if user exist and have a scrum master classification in projectUsers field
    def validate(self, attrs):
        users = attrs.get('projectUsers')
        found_scrum_master = False
        for user in users:
            username = user.get('user').get('username')
            try:
                User.objects.get(username=username)
                classification = user.get('classification')
                if classification == UserProject.Classification.SCRUM_MASTER:
                    found_scrum_master = True
                    break
            except:
                pass
        if not found_scrum_master:
            raise serializers \
                .ValidationError({'Status': "Please choice at least a exiting user with Scrum master classification"})
        return attrs

    def create(self, validated_data):
        authenticated_user = self.get_authenticated_user()
        project_users_data = validated_data.pop('projectUsers')
        project = Project.objects.create(**validated_data)
        # self.save_authenticed_user(authenticated_user, project)
        return self.get_saved_project(authenticated_user, project, project_users_data)

    def update(self, instance, validated_data):
        authenticated_user = self.get_authenticated_user()
        project_users_data = validated_data.pop('projectUsers')

        instance.code = validated_data.get('code', instance.code)
        instance.designation = validated_data.get(
            'designation', instance.designation)
        instance.objective = validated_data.get(
            'objective', instance.objective)
        instance.save()

        user_projects = UserProject.objects.filter(project=instance)
        user_projects.delete()
        # self.save_authenticed_user(authenticated_user, instance)

        return self.get_saved_project(authenticated_user, instance, project_users_data)

    def get_saved_project(self, authenticated_user, project, project_users_data):
        for project_user_data in project_users_data:
            username = project_user_data.get('user').get('username')
            classification_input = project_user_data.get('classification')

            try:
                user = User.objects.get(username=username)
                if user and user.is_active and not user.is_superuser:
                    user_project = UserProject(user=user, project=project,
                                               classification=classification_input)
                    user_project.save()
            except Exception as e:
                pass

        return project

    def get_authenticated_user(self):
        authenticated_user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            authenticated_user = User.objects.get(username=request.user)
        return authenticated_user


"""
user = UserSerializer(many=False, read_only=True)
    user_id = serializers.IntegerField(write_only=True)
"""


# Sprint serializer
class SprintSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(many=False, read_only=True)
    # code_project = serializers.CharField(write_only=True)

    class Meta:
        model = Sprint
        fields = "__all__"

    def validate(self, attrs):
        project_to_found = attrs.get('project')
        authenticated_user = self.get_authenticated_user()
        try:
            # check if the authenticated user is participate to this project
            user_project = UserProject.objects.filter(
                user=authenticated_user, project=project_to_found).get()
        except:
            # the authenticated user can't add sprint to this project so return not found
            raise serializers.ValidationError({'Project': "Project not found"})
        return attrs

    def get_authenticated_user(self):
        authenticated_user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            authenticated_user = User.objects.get(username=request.user)
        return authenticated_user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data):
        # Check that start_at is before end_at.
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError(
                {'Date': "La date de fin doit etre superieur au date de debut"})
        # Check if the sprint is planifie ou en cours
        if data['sprint'].status not in ['Planifiè', 'En Cours']:
            raise serializers \
                .ValidationError({'Sprint': "the status of the sprint must be Planifie ou En cours"})
        user = data['user']
        sprint = data['sprint']
        project = sprint.project
        users = project.users.all()
        if user not in users:
            raise serializers.ValidationError(
                {'user': "This user does not belong to this sprint"})
        return data


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

    def update(self, instance, validated_data):
        status = instance.status
        # only update the document that their status are ACTUAL
        if status == 'EX':
            raise serializers \
                .ValidationError({'Document': 'cannot modify this document because it is out of date'})
        return super().update(instance, validated_data)


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"

    def validate(self, data):
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError(
                {'date': "The end date must be greater than the start date"})
        task = data['task']
        if task.user != self.get_authenticated_user():
            raise serializers.ValidationError(
                {'tache': "cannot add this problem"})
        return data

    def get_authenticated_user(self):
        authenticated_user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            authenticated_user = User.objects.get(username=request.user)
        return authenticated_user
