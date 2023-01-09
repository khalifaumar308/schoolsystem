from rest_framework import serializers
from .models import TeacherAccount, OtherUser
from .utils import generate_username
from django.utils.crypto import get_random_string 
from django.db import transaction
from .functions import send_mailer


class OtherUserSerializer(serializers.ModelSerializer):
    STATES = (
                ("ABIA","Abia"),
                ("ADAMAWA","Adamawa"),
                ("AKWA-IBOM","AkwaIbom"),
                ("ANAMBRA","Anambra"),
                ("BAUCHI","Bauchi"),
                ("BAYELSA","Bayelsa"),
                ("BENUE","Benue"),
                ("BORNO","Borno"),
                ("CROSS-RIVER","CrossRiver"),
                ("DELTA","Delta"),
                ("EBONYI","Ebonyi"),
                ("EDO","Edo"),
                ("EKITI","Ekiti"),
                ("ENUGU","Enugu"),
                ("GOMBE","Gombe"),
                ("IMO","Imo"),
                ("JIGAWA","Jigawa"),
                ("KADUNA","Kaduna"),
                ("KANO","Kano"),
                ("KATSINA","Katsina"),
                ("KEBBI","Kebbi"),
                ("KOGI","Kogi"),
                ("KWARA","Kwara"),
                ("LAGOS","Lagos"),
                ("NASSARAWA","Nassarawa"),
                ("NIGER","Niger"),
                ("OGUN","Ogun"),
                ("ONDO","Ondo"),
                ("OSUN","Osun"),
                ("OYO","Oyo"),
                ("PLATEAU","Plateau"),
                ("RIVERS","Rivers"),
                ("SOKOTO","Sokoto"),
                ("TARABA","Taraba"),
                ("YOBE","Yobe"),
                ("ZAMFARA","Zamfara"),
                ("FCT-ABUJA","FctAbuja"),
    )
    country = serializers.CharField(default="Nigeria")
    state = serializers.ChoiceField(choices=STATES)
    # pin = serializers.CharField()
    class Meta:
        model = OtherUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'roles', 'country', 'state']

    @classmethod
    def create(cls, validated_data):
        print("🚀 ~ file: serializers.py:15 ~ validated_data", validated_data)
        country = validated_data.pop('country')
        state = validated_data.pop('state')

        with transaction.atomic():
            other_user = OtherUser.objects.create(**validated_data)

            if other_user.roles == 'Teacher':
                username = generate_username('Teacher')
                pin = get_random_string(length=6, allowed_chars="1234567890")
                first_name = validated_data.get("first_name")
                last_name = validated_data.get("last_name")
                middle_name = validated_data.get("middle_name")
                email = validated_data.get("email")
                print('ITEMS')
                print(first_name, last_name, email)
                mail_data = dict(
                            recipient = email,
                            message=f"WELCOME here is your username {username} and otp {pin}"
                        )
                send_mailer(**mail_data)
                TeacherAccount.create_account(
                    username=username, 
                    country=country,
                    state=state,
                    pin = pin,
                    other_user = other_user

                )
                print('USERNAME AND PIN')
                print(username, pin)

        print("***********VALIDATED DATA")
        print(validated_data)
        print("###############OTHER USER")
        print(other_user, pin, username)
        return other_user
class TeacherAccountSerializer(serializers.ModelSerializer):
    # username = serializers.CharField()
    # country = serializers.CharField()
    # state = serializers.CharField()
    class Meta:
        model = TeacherAccount
        fields = ('id', 'country', 'state', 'username', 'other_user')
        read_only_fields = ('other_user','id')
    

    def update(self, instance, validated_data):
        print("🚀 ~ file: serializers.py:47 ~ validated_data", validated_data)
        print("🚀 ~ file: serializers.py:47 ~ instance", instance)
        # Load the state and country fields with the saved data
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        # Update the other fields
        # instance.username = validated_data.get('username', instance.username)
        # instance.other_user = validated_data.get('other_user', instance.other_user)
        # Save the changes
        instance.save()
        return instance

    # def create(self, validated_data):
    #     # generate unique username for the teacher
    #     username = generate_username('teacher')

    #     new_teacher = TeacherAccount.create_account(
    #         username=username,
    #         country=validated_data['country'],
    #         state=validated_data['state'],
    #     )

    #     return new_teacher