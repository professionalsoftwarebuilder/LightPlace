from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from core.models import Profile
from . models import Chat
import json

def index(request):
    return render(request, 'index.html')

@login_required
def room(request, room_name):
    # Get profile record of current user
    usrProfile = Profile.objects.get(prf_User=request.user)
    # Get all the users to create a search list
    usrModel = get_user_model()
    allUsers = usrModel.objects.exclude(id=request.user.id)
    userChats = Chat.objects.filter(Contacts=usrProfile)

    theUsername = request.user.username

    print('room view username: ' + theUsername)

    return render(request, 'room.html', {
        #'room_name_json': mark_safe(json.dumps(room_name)),
        'room_name': room_name,
        #'theUsername': mark_safe(json.dumps(request.user.username)),
        'theUsername': theUsername,
        'usrProfile': usrProfile,
        'allContacts': allUsers,
        'userChats': userChats
    })

@login_required
def list_contacts(request):
    # Get profile record of current user
    usrProfile = Profile.objects.get(prf_User=request.user)
    # Get all the users to create a search list
    usrModel = get_user_model()
    allUsers = usrModel.objects.exclude(id=request.user.id)

    return render(request, 'list_contacts.html', {
        'username': mark_safe(json.dumps(request.user.username)),
        'usrProfile': usrProfile,
        'allContacts': allUsers
    })


@login_required
def create_dialog_chat(request, cont_id):
    # Create the chat:

    # Get profile record of current user
    usrProfile = Profile.objects.get(prf_User=request.user)
    # Get the interlocutor profile object
    usrModel = get_user_model()
    intrlUser = usrModel.objects.get(id=cont_id)
    intrlProfile = Profile.objects.get(prf_User=intrlUser)
    # Create name of chat
    chatName = usrProfile.prf_User.username + '_' + intrlUser.username
    # Create new chat object an save
    newChat = Chat.objects.create(cht_Name=chatName)
    # Add user aan contact to chat
    newChat.Contacts.add(usrProfile)
    newChat.Contacts.add(intrlProfile)
    # Redirect to room (view)
    return redirect('chat:room', chatName)

