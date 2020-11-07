import PySimpleGUI as sg
import json

CurrentUser = None
Profiles = []


class User:
    def __init__(self, user_email, user_name, user_location, user_bio, user_hobbies, user_friends=[]):
        self.email = user_email
        self.name = user_name
        self.location = user_location
        self.hobbies = user_hobbies
        self.friends = user_friends
        self.bio = user_bio


layout_sign_in = [
    [sg.Text("Email", size=(50,1)), sg.InputText(key='email')],
    [sg.Text("Password", size=(50,1)), sg.InputText(key='password', password_char='*')],
    [sg.Button(button_text='Login'), sg.Button(button_text='Do not have an account? Sign Up')]
]

num_hobbies = 5;
layout_sign_up = [
    [sg.Text("Email", size=(50,1)), sg.InputText(key='signup_email')],
    [sg.Text("Password", size=(50,1)), sg.InputText(key='signup_password', password_char='*')],
    [sg.Text("Name", size=(50, 1)), sg.InputText(key='signup_name')],
    [sg.Text("Location", size=(50, 1)), sg.InputText(key='signup_location')],
    [sg.Text("Bio", size=(50, 1)), sg.InputText(key='signup_bio')],
    *[[sg.Text(f"Hobby {i + 1}"), sg.InputText(key=f'signup_hobby_{i + 1}')] for i in range(num_hobbies)],
    [sg.Button(button_text='Sign Up'), sg.Button(button_text='Already have an account? Sign In')]
]

layout = [
    [sg.Column(layout_sign_in, key='sign_in_layout'), sg.Column(layout_sign_up, visible=False, key='sign_up_layout')]
]

window = sg.Window('App', layout)

def connection_strength(user_1,user_2):
    strength = 0

    if user_2.location == user_1.location:
        strength += 20

    for friend in user_2.friends:
        if friend in user_1.friends:
            strength += 10

    for hobby in user_2.hobbies:
        if hobby in user_1.hobbies:
            strength += 5

    return strength


def home_screen():

    print(Profiles)
    unknown_profiles = Profiles
    print(f'length: {len(Profiles)}')
    for x in Profiles:
        for y in CurrentUser.friends:
            if x == y:
                unknown_profiles.remove(x)
    print(unknown_profiles)

    suggested_profile = [[0, 0], [0, 0], [0, 0]]
    for x in unknown_profiles:
        print(x.location)
        strength = connection_strength(CurrentUser, x)
        if strength > suggested_profile[2][0]:
            if strength > suggested_profile[1][0]:
                if strength > suggested_profile[0][0]:
                    suggested_profile[0][1] = x
                else:
                    suggested_profile[1][0] = x
            else:
                suggested_profile[2][0] = x

    print(f'length: {len(unknown_profiles)}')
    layout_home = [
        [sg.Text(CurrentUser.name, size=(25, 1))],
        [sg.Text(CurrentUser.bio, size=(25, 3))],
        [sg.Text(CurrentUser.location, size=(25, 1))],
        [sg.Text('Suggested Friends', size=(25, 1))],
        *[[sg.Text(unknown_profiles[i].name, size=(13, 1)), sg.Text(unknown_profiles[i].location, size=(12, 1))] for i in range(len(unknown_profiles))]
    ]
    home_window = sg.Window('Home', layout_home)

    while True:
        home_event, home_values = home_window.read()
        if home_event is None:
            break


while True:
    event, values = window.read()
    print(event)
    if event is None:
        break
    if event == 'Do not have an account? Sign Up':
        window[f'sign_in_layout'].update(visible=False)
        window[f'sign_up_layout'].update(visible=True)
    if event == 'Already have an account? Sign In':
        window[f'sign_in_layout'].update(visible=True)
        window[f'sign_up_layout'].update(visible=False)
    if event == 'Sign Up':
        email = values['signup_email']
        password = values['signup_password']

        name = values['signup_name']
        location = values['signup_location']
        bio = values['signup_bio']
        hobbies = [] * num_hobbies
        for i in range(0, num_hobbies):
            hobbies.append(values[f'signup_hobby_{i + 1}'])

        CurrentUser = User(email, name, location, bio, hobbies)

        print(CurrentUser)

        account_info = {}
        profiles = {}

        with open('Auth.txt') as json_file:
            account_info = json.load(json_file)
            account_info['accounts'].append({
                'email': email,
                'password': password
            })
        with open('Auth.txt', 'w') as outfile:
            json.dump(account_info, outfile)

        with open('Profile.txt') as json_file:
            profiles = json.load(json_file)
            profiles['profile'].append({
                'email': CurrentUser.email,
                'name': CurrentUser.name,
                'location': CurrentUser.location,
                'bio': CurrentUser.bio,
                'hobbies': CurrentUser.hobbies,
                'friends': []
            })
        with open('Profile.txt', 'w') as outfile:
            json.dump(profiles, outfile)

    if event == 'Login':
        email = values['email']
        password = values['password']

        Accounts = {}

        with open('Auth.txt') as json_file:
            Accounts = json.load(json_file)

        for account in Accounts['accounts']:
            if account['email'] == email:
                if account['password'] == password:
                    print('login success')

        with open('Profile.txt') as json_file:
            temp = json.load(json_file)
            print(temp['profile'])
            print(len(temp['profile']))
            for profile in temp['profile']:
                print('ddd')
                if profile['email'] == email:
                    CurrentUser = User(email, profile['name'], profile['location'], profile['bio'], profile['hobbies'], profile['friends'])
                    window.close()
                    home_screen()
                else:
                    print('hhhh')
                    Profiles.append(User(email, profile['name'], profile['location'], profile['bio'], profile['hobbies'], profile['friends']))










