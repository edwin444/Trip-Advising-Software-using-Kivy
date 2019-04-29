#!/usr/bin/python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import kivy
kivy.require('1.8.0')
import pickle
import os
import datetime
import itertools
import smtplib
from kivy.app import App
from email.mime.text import MIMEText
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.graphics import BorderImage
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.slider import Slider
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.image import AsyncImage, Image
from kivy.graphics import *
printpath = []
printflightmain = []
all_comb = []
time_list = []
dep_plane_list = []

return_printpath = []
return_printflightmain = []
return_all_comb = []
return_time_list = []
return_plane_list = []

g = []

Email_id = ""                # Stores email id of user
fromin = TextInput(text='')
toin = TextInput(text='')
depin = TextInput(text='')
arrin = TextInput(text='')
searchpage = []
seatmatrix = []
flightmain = []
entry_index = -1
return_entry_index = -1
unprocessed_list = []  # unprocessed_list holds the plane objects in order
countseatmatrix = 0
return_unprocessed_list = []
return_countseatmatrix = 0
deptoreturn = 0
enter_names = []
username = []
boardingpass = []
count = 0
return_count = -1
chosen_seats = {}
return_chosen_seats = {}
chosen_seats_count = 0
return_chosen_seats_count = 0
boarding_pass_page_reached = 0
return_true = 0  # Check wheteher return flight is booked or not
total_persons = 0
mainadropdown = 0
maincdropdown = 0
mainidropdown = 0
names_objects_list = []
names_list = []
names_iterator = 0
adropdown = []
cdropdown = []
idropdown = []

usernamelogin = TextInput(text='', multiline=False, size_hint=(0.3,
                          0.05), pos=(220, 350))
passwordlogin = TextInput(password=True, password_mask='*',
                          multiline=False, size_hint=(0.3, 0.05),
                          pos=(220, 270))

usernamesignup = TextInput(text='', multiline=False, size_hint=(0.3,
                           0.05), pos=(460, 425))
passwordsignup = TextInput(password=True, multiline=False,
                           size_hint=(0.3, 0.05), pos=(460, 350))
emailidsignup = TextInput(text='', multiline=False, size_hint=(0.3,
                          0.05), pos=(460, 270))
mobilenosignup = TextInput(text='', multiline=False, size_hint=(0.3,
                           0.05), pos=(460, 185))


# this class is used to create nodes in the graph which is synonymous to locations

class node:

    def __init__(self, name):
        self.node_name = name
        self.adj_node = {}
        self.plane_array = []

    def update_plane_array(self, plane):  # Plane objects are added into the array
        self.plane_array.append(plane)

    def create_neighbour(self, name, weight):  # weight is time in minutes
        self.adj_node[name] = weight

    def get_adj_nodes(self):
        return self.adj_node.keys()

    def get_name(self):
        return self.node_name

    def get_plane_array(self):
        return self.plane_array

    def get_weight(self, name):
        return self.adj_node[name]


# this class is used to define a graph containing many node objects
# it contains the no of nodes and also the a dictionary containing the name_of_vertices as key and the node object as the value of that
# key in the dictionary
# So, basically it stores all the vertices objects of the node class in a graph object

class graph:

    def __init__(self):
        self.no_of_vertices = 0
        self.vertices = {}

    def add_vertex(self, name):
        new_vertex = node(name)
        self.vertices[name] = new_vertex
        return new_vertex

    def search_vertex(self, name):
        return self.vertices[name]

# When user enters the route of plane, the plane objects will be stored in the nodes along the route of the plane       ....    ........

    def add_planes_to_nodes(self, plane, node_name):
        node = self.search_vertex(node_name)
        node_plane_array = node.get_plane_array()
        if plane not in node_plane_array:
            node.update_plane_array(plane)

    def get_num_vertices(self):
        return self.no_of_vertices

    def get_vertices(self):
        return self.vertices

    def add_edge(
        self,
        fromm,
        to,
        weight,
        ):

        if fromm not in self.vertices:
            self.vertices.add_vertex(fromm)
        if to not in self.vertices:
            self.vertices.add_vertex(to)

        self.vertices[fromm].create_neighbour(to, weight)
        self.vertices[to].create_neighbour(fromm, weight)


class admin:

    def __init__(self):

        self.name = 'abc'
        self.email_id = 'abc'
        self.password = '123'
        self.company_name = '123'

    def modify(
        self,
        name,
        email,
        password,
        company,
        ):

        self.name = name
        self.email_id = email
        self.password = password
        self.company_name = company


# customer class is used to store customer objects and their related information.

class customer:

    def __init__(self):

        self.name = 'abc'
        self.email_id = '123'
        self.phone_number = 1234
        self.password = '1243'

    def modify(
        self,
        name,
        email,
        password,
        phone_number,
        ):

        self.name = name
        self.email_id = email
        self.password = password
        self.phone_number = phone_number


# the plane class is used to store plane objects with different information regarding
# route it takes, the start time and seating_matrix and the duration of the flight trip
# helper function exists to calculate the status of the flight at any time entered.

class plane:

    def __init__(self):
        self.start_time = 0  # 0 minutes refers to 12 a.m.
        self.start_date = '12/2/2018'
        self.route = []  # Route stores the names of the nodes involved in the trip
        self.duration = 0  # duration stores the total duration of one round in minutes
        self.seating_matrix = {}  # [[0 for j in range(4)] for i in range(15)]
        self.plane_no = 123
        self.company_name = 'abc'

    def modify_plane(
        self,
        start_time,
        start_date,
        route,
        plane_no,
        company_name,
        graph,
        ):

        self.start_time = start_time
        self.start_date = start_date
        self.route = route
        self.plane_no = plane_no
        self.company_name = company_name
        for i in range(0, len(route)):
            graph.add_planes_to_nodes(self, route[i])

    def find_duration(self, graph):
        self.duration = 0  # duration should be specified in minutes
        j = 'abc'
        for i in self.route:
            node = graph.search_vertex(i)
            if j != 'abc':
                self.duration += node.get_weight(j)
            j = i
        self.duration += node.get_weight(self.route[0])

    def position_determiner(  # Current time should be in minutes
        self,
        current_time,
        current_date,
        graph,
        ):

        current_date_list_ddmmyy = current_date.split('/')
        start_date_list_ddmmyy = self.start_date.split('/')

        start_day = int(start_date_list_ddmmyy[0])
        start_month = int(start_date_list_ddmmyy[1])
        start_year = int(start_date_list_ddmmyy[2])

        current_day = int(current_date_list_ddmmyy[0])
        current_month = int(current_date_list_ddmmyy[1])
        current_year = int(current_date_list_ddmmyy[2])

        cd = datetime.datetime(current_year, current_month,
                               current_day, current_time / 60,
                               current_time % 60)
        sd = datetime.datetime(start_year, start_month, start_day,
                               self.start_time / 60, self.start_time
                               % 60)

        difference = cd - sd

        difference_minutes = difference.days * 24 * 60 \
            + difference.seconds / 60

        self.find_duration(graph)

        etfs = difference_minutes % self.duration  # Elapsed time from start

        j = 'abc'

        for i in self.route:
            s = graph.search_vertex(i)
            if j != 'abc':
                etfs -= s.get_weight(j)
            j = s.get_name()
            if etfs == 0:
                return (1, s.get_name())

        return (0, 'Arbitrary value')

    def return_time(  # Current time should be in minutes
        self,
        current_date,
        node,
        graph,
        ):

        current_date_list_ddmmyy = current_date.split('/')
        start_date_list_ddmmyy = self.start_date.split('/')

        start_day = int(start_date_list_ddmmyy[0])
        start_month = int(start_date_list_ddmmyy[1])
        start_year = int(start_date_list_ddmmyy[2])

        current_day = int(current_date_list_ddmmyy[0])
        current_month = int(current_date_list_ddmmyy[1])
        current_year = int(current_date_list_ddmmyy[2])

        cd = datetime.datetime(current_year, current_month,
                               current_day, 0, 0)
        sd = datetime.datetime(start_year, start_month, start_day,
                               self.start_time / 60, self.start_time
                               % 60)

        difference = cd - sd

        difference_minutes = difference.days * 24 * 60 \
            + difference.seconds / 60

        self.find_duration(graph)

        etfs = difference_minutes % self.duration  # Elapsed time from start
        st = cd - datetime.timedelta(minutes=etfs)  # start time

        list_time = []
        counter = st
        while counter < cd + datetime.timedelta(days=1):
            j = 'abc'
            for i in self.route:
                current_node = graph.search_vertex(i)
                if j != 'abc':
                    counter = counter \
                        + datetime.timedelta(minutes=current_node.get_weight(j))
                if i == node.get_name() and counter >= cd and counter \
                    < cd + datetime.timedelta(days=1):
                    temp = counter
                    list_time.append(temp)
                j = i
            counter += \
                datetime.timedelta(minutes=current_node.get_weight(self.route[0]))

        return list_time


# the algorithm used to check all the available planes from one node to the other

def printAllPathsUtil(
    u,
    d,
    visited_nodes_dict,
    all_paths,
    path,
    graph,
    ):

        # here we mark the node as visited iff all the planes that can take that edge possibility has been considered

    visited_nodes_dict[u] = 1
    path.append(u)

        # If current vertex is same as destination, then print
        # current path[]

    if u.get_name() == d.get_name():
        temp = path[:]
        all_paths.append(temp)
    else:

            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex

        adj_arr = u.get_adj_nodes()
        for n in adj_arr:
            i = graph.search_vertex(n)
            if visited_nodes_dict[i] == 0:
                printAllPathsUtil(
                    i,
                    d,
                    visited_nodes_dict,
                    all_paths,
                    path,
                    graph,
                    )

        # Remove current vertex from path[] and mark it as unvisited

    path.pop()
    visited_nodes_dict[u] = 0


    # Prints all paths from 's' to 'd'

def printAllPaths(s, d, graph):  # s and d are node objects

    node_dict = graph.get_vertices()
    nodes = node_dict.values()
    visited_nodes_dict = {}
    for i in nodes:
        visited_nodes_dict[i] = 0

        # Create an array to store paths

    all_paths = []  # all_paths is a 2d matrix storing all the paths
    path = []  # path is an array storing the current path

        # Call the recursive helper function to print all paths

    printAllPathsUtil(
        s,
        d,
        visited_nodes_dict,
        all_paths,
        path,
        graph,
        )
    return all_paths


# the search flights function is used to search all flights from the source to destination entered by the user and
# display the possible sequence or combinations to reach from the source to destination.

def search_flights(all_paths, current_date, graph):
    path_list = []
    plane_list = []
    next = 1
    for path in all_paths:
        path_list = []
        for n in path[0].plane_array:
            string = ''.join(n.route) + n.route[0]
            l = n.return_time(current_date, path[0], graph)  # l is a list of datetime objects
            if str(path[0].node_name) + str(path[1].node_name) \
                in string and l != []:

            # Checking if current node and next node is consecutively present in the route of the plane

                cur_time = l[0]  # curtime is a datetime object fot the first occurrence of plane

                # print 'cuureytie ',cur_time,'\n'                         # next_node is object

                time = cur_time \
                    + datetime.timedelta(minutes=path[0].get_weight(path[1].node_name))
                count = 0
                next = 1

                # time stores the expected time at which the plane arrives at the next node w.r.t to the path

                plane_arr1 = []
                plane_arr1.append([path[0].node_name + str(n.plane_no)
                                  + n.company_name])
                while count <= len(path) - 3:
                    planes = []

                    next_node = path[next]

                    time_temp = time

                    time = time \
                        + datetime.timedelta(minutes=next_node.get_weight(path[next
                            + 1].node_name))

                    prev_date = str(time_temp.day) + '/' \
                        + str(time_temp.month) + '/' \
                        + str(time_temp.year)
                    time_temp_min = time_temp.hour * 60 \
                        + time_temp.minute

                    new_date = str(time.day) + '/' + str(time.month) \
                        + '/' + str(time.year)
                    time_min = time.hour * 60 + time.minute

                    for j in path[next].plane_array:

                        (prev_status, str_prev_place) = \
                            j.position_determiner(time_temp_min,
                                prev_date, graph)
                        (status, str_place) = \
                            j.position_determiner(time_min, new_date,
                                graph)
                        if status == 1 and str_place == path[next
                                + 1].node_name and path[next].node_name \
                            == str_prev_place:
                            planes.append(path[next].node_name
                                    + str(j.plane_no) + j.company_name)

                    next = next + 1
                    count = count + 1
                    plane_arr1.append(planes[:])
                if [] not in plane_arr1:
                    path_list.append(plane_arr1[:])

        if path_list != []:
            plane_list.append(path_list[:])

    return plane_list


# this class is used to represent the home page logo of the application

class ScreenOne(Screen):

    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)

        l = FloatLayout(orientation='vertical')

        # l1 = FloatLayout(orientation='vertical')

        # button2 = Button(text='Admin', size_hint=(0.1, 0.1), pos=(900,
        #                 600))

        button1 = Button(text='User', size_hint=(0.2, 0.3),
                         pos_hint={'x': 0.4, 'y': 0.35})  # pos=(445,200)

        # l1 is for the icon
        # l is for the background image of the app

        l.add_widget(button1)

        l.add_widget(AsyncImage(source='homepage.png',
                     allow_stretch=True, keep_ratio=False,
                     size_hint=(1.0, 1.0), pos_hint={'center_x': .5,
                     'center_y': .5}))

        button1.bind(on_press=self.changerforuser)

        self.add_widget(l)

    def changerforadmin(self, *args):
        self.manager.current = 'screen2'

    def changerforuser(self, *args):
        self.manager.current = 'screen2'


# this is the users login page

class ScreenTwo(Screen):

    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)

        f1 = FloatLayout(orientation='vertical')
        f2 = FloatLayout(orientation='vertical')

        # this is for background image of the user login page

        im = AsyncImage(source='tajmahal.jpg', size_hint=(1.2, 1.1),
                        pos_hint={'center_x': .5, 'center_y': .5})
        f1.add_widget(im)
        f2.add_widget(AsyncImage(source='https://images.designtrends.com/wp-content/uploads/2015/11/13152944/Artistic-Gray-Wallpaper-for-Desktop1.jpg'
                      , size_hint=(.5, .5), pos_hint={'center_x': .5,
                      'center_y': .5}))

        with im.canvas:
            Color(0, 0, 0, 0.3)
            Rectangle(pos=(200, 150), size=(400, 300))
            size_hint = (1.0, 1.0)

        # this is for the username

        label1 = Label(text='[b]Username[/b]', size_hint=(0.1, 0.1),
                       markup=True, pos=(220, 375))

        # this label is used for the password

        label2 = Label(text='[b]Password[/b]', markup=True,
                       size_hint=(0.1, 0.1), pos=(220, 290))

        # button for login access

        buttonenter = Button(text='Login', size_hint=(0.2, 0.07),
                             pos=(225, 200), background_color=(0, 1, 0,
                             0.8))

        # this is the button used for sign up

        buttonsignup = Button(text='Not a User?(Sign up)',
                              size_hint=(0.2, 0.07), pos=(420, 200),
                              background_color=(1, 0, 0, 0.8))

        # button used to go back

        buttongoback = Button(text='Go Back', size_hint=(0.2, 0.07),
                              pos=(10, 550), background_color=(0, 0, 0,
                              0.3))

        # f1.add_widget(f2)

        f1.add_widget(label1)
        f1.add_widget(label2)
        f1.add_widget(usernamelogin)
        f1.add_widget(passwordlogin)
        f1.add_widget(buttonenter)
        f1.add_widget(buttonsignup)
        f1.add_widget(buttongoback)

        buttonsignup.bind(on_press=self.signupchanger)
        buttonenter.bind(on_press=self.loginchanger)
        buttongoback.bind(on_press=self.gobackchanger)

        self.add_widget(f1)

    def gobackchanger(self, *args):
        global usernamelogin
        global passwordlogin
        usernamelogin.text = ''
        usernamelogin.hint_text = ''
        passwordlogin.text = ''
        passwordlogin.hint_text = ''
        self.manager.current = 'screen1'

    def loginchanger(self, *args):
        global username  # Global variable to store username of user
        global usernamelogin
        global passwordlogin
        global Email_id
        flag = 1
        try:
            f = open('userlogintest2.dat', 'rb')
            while True:
                s = pickle.load(f)
                if usernamelogin.text == s.name and passwordlogin.text \
                    == s.password:
                    Email_id = s.email_id
                    flag = 0
        except EOFError:
            if flag == 0:
                flag = 1
                global username  # Global variable to store username of user
                username = usernamelogin.text[:]
                usernamelogin.text = ''
                usernamelogin.hint_text = ''
                passwordlogin.text = ''
                passwordlogin.hint_text = ''
                f.close()
                self.manager.current = 'optionpage'
            else:

                usernamelogin.text = ''
                usernamelogin.hint_text = 'Account doesnt exist'
                usernamelogin.hint_text_color = (1, 0, 0, 0.7)

                passwordlogin.hint_text = 'Enter again'
                passwordlogin.text = ''
                passwordlogin.hint_text_color = (1, 0, 0, 0.7)
                f.close()
                self.manager.current = 'screen2'

    def signupchanger(self, *args):
        global usernamelogin
        global passwordlogin
        usernamelogin.text = ''
        usernamelogin.hint_text = ''
        passwordlogin.text = ''
        passwordlogin.hint_text = ''
        self.manager.current = 'screenusersignup'


# This is the screen for usersign up page

class Screenusersignup(Screen):

    def __init__(self, **kwargs):

        super(Screenusersignup, self).__init__(**kwargs)
        f1 = FloatLayout(orientation='vertical')
        f2 = FloatLayout(orientation='vertical')

            # this is for background image of the user login page

        f1.add_widget(AsyncImage(source='usersignup.jpg',
                      size_hint=(8.0, 8.0), pos_hint={'center_x': .5,
                      'center_y': .5}))

            # this is for creating the image on which the the user details will
            # be entered..

        f2.add_widget(AsyncImage(source='gray.jpg', size_hint=(0.42,
                      1.4), pos_hint={'center_x': 0.74,
                      'center_y': .5}))

            # this is for the username

        label1 = Label(text='Username', size_hint=(0.1, 0.1), pos=(460,
                       445))

            # this label is used for the password

        label2 = Label(text='Password', size_hint=(0.1, 0.1), pos=(460,
                       375))

        label3 = Label(text='Email-id', size_hint=(0.1, 0.1), pos=(455,
                       290))

        label4 = Label(text='Mobile Number', size_hint=(0.1, 0.1),
                       pos=(480, 205))

            # button for login access

        buttonregister = Button(text='Register', size_hint=(0.2, 0.09),
                                pos=(500, 100))

            # button used to go back

        buttongoback = Button(text='Go Back', size_hint=(0.2, 0.07),
                              pos=(10, 550), background_color=(0, 0, 0,
                              .5))

        # setting the text hints back to empty when come from login page

        f1.add_widget(f2)
        f1.add_widget(label1)
        f1.add_widget(label2)
        f1.add_widget(label3)
        f1.add_widget(label4)
        f1.add_widget(usernamesignup)
        f1.add_widget(passwordsignup)
        f1.add_widget(emailidsignup)
        f1.add_widget(mobilenosignup)

        f1.add_widget(buttonregister)

        f1.add_widget(buttongoback)

        buttonregister.bind(on_press=self.registerchanger)
        buttongoback.bind(on_press=self.gobackchanger)

        self.add_widget(f1)

    def gobackchanger(self, *args):
        global usernamesignup
        global passwordsignup
        global emailidsignup
        global mobilenosignup
        usernamesignup.hint_text = ''
        passwordsignup.hint_text = ''
        emailidsignup.hint_text = ''
        mobilenosignup.hint_text = ''
        self.manager.current = 'screen2'

    def registerchanger(self, *args):

        global usernamesignup
        global passwordsignup
        global emailidsignup
        global mobilenosignup

        f = open('userlogintest2.dat', 'ab+')
        flag = 0
        flagempty = 0
        try:
            #-------------------checking condition for email-----------------------
            fromaddr = 'pythonpython4444@gmail.com'

            toaddrs = str(emailidsignup.text)

            SMTPServer = 'smtp.gmail.com'

            port = 465 #587

            login = "pythonpython4444@gmail.com"

            password = "pythonpython"


            dummy_var = 2;
            text_to_send = "Test for registeration To Ascend..."
                  
            try:
                msg = MIMEText(text_to_send)

                #msgtxt = "http://www.google.com"+"\n\n"+"This is a test."

                #msg.set_content(msgtxt)

                msg['Subject'] = "Test message"

                msg['From'] = fromaddr

                msg['To'] = toaddrs



                server = smtplib.SMTP_SSL(SMTPServer, port) #use smtplib.SMTP() if port is 587

                #server.startssl()

                server.login(login, password)

                server.sendmail(fromaddr, toaddrs, msg.as_string())

                server.quit()
            except:
                flagempty= 1



            #---------------------------------------------------------------------
            if usernamesignup.text.isspace() == True \
                or passwordsignup.text.isalnum() == False \
                or len(emailidsignup.text) == 0 \
                or mobilenosignup.text.isalnum() == False:
                flagempty = 1

            while True:

                s = pickle.load(f)
                if usernamesignup.text == s.name:
                    flag = 1
        except EOFError:

            # it means the user doesnt exist

            if flagempty == 1:
                flagempty = 0

                usernamesignup.text = ''
                usernamesignup.hint_text = '**Required field**'
                usernamesignup.hint_text_color = (1, 0, 0, 0.7)

                passwordsignup.text = ''
                passwordsignup.hint_text = '**Required field**'
                passwordsignup.hint_text_color = (1, 0, 0, 0.7)

                emailidsignup.text = ''
                emailidsignup.hint_text = '**Required field**'
                emailidsignup.hint_text_color = (1, 0, 0, 0.7)

                mobilenosignup.text = ''
                mobilenosignup.hint_text = '**Required field**'
                mobilenosignup.hint_text_color = (1, 0, 0, 0.7)

                f.close()
                self.manager.current = 'screenusersignup'
            elif flag == 0:

                c = customer()
                c.modify(usernamesignup.text, emailidsignup.text,
                         passwordsignup.text, mobilenosignup.text)
                pickle.dump(c, f)
                usernamesignup.text = ''
                passwordsignup.text = ''
                emailidsignup.text = ''
                mobilenosignup.text = ''
                usernamesignup.hint_text = ''
                passwordsignup.hint_text = ''
                emailidsignup.hint_text = ''
                mobilenosignup.hint_text = ''
                f.close()
                self.manager.current = 'screen2'
            elif flag == 1:
                flag = 0
                usernamesignup.text = ''
                usernamesignup.hint_text = 'User name already exists'
                usernamesignup.hint_text_color = (1, 0, 0, 0.7)

                passwordsignup.text = ''
                passwordsignup.hint_text = 'Please enter again'
                passwordsignup.hint_text_color = (1, 0, 0, 0.7)

                emailidsignup.text = ''
                emailidsignup.hint_text = 'Please enter again'
                emailidsignup.hint_text_color = (1, 0, 0, 0.7)

                mobilenosignup.text = ''
                mobilenosignup.hint_text = 'Please enter again'
                mobilenosignup.hint_text_color = (1, 0, 0, 0.7)

                f.close()
                self.manager.current = 'screenusersignup'


# this is the option page showing choice for flights

class OptionPage(Screen):

    def __init__(self, **kwargs):
        super(OptionPage, self).__init__(**kwargs)

        f1 = FloatLayout(orientation='vertical')
        f2 = FloatLayout(orientation='vertical')

        im = AsyncImage(source='sky.jpg', size_hint=(1.0, 1.0),
                        pos_hint={'x': 0, 'y': 0})  # source = "https://ak5.picdn.net/shutterstock/videos/804505/thumb/1.jpg?i10c=img.resize(height:160)",

                # allow_stretch = True

        f2.add_widget(im)

        label1 = \
            Label(text='''[b]
                         \"An investment in travelling 
                          is an investment in yourself\"
                          ~Matthew Karsten.
                          \"Stuff your eyes with wonder 
                          and live as if you would drop 
                          dead in 10 seconds.
                          See the world its more fantastic 
                          than any dream made or paid in 
                          factories.\"
                          ~Ray Bradberry.
                          \"Travelling first makes you 
                          speechless then it turns you 
                          into a storyteller\"
                           ~Ibn Bathutha
                           [/b]''',
                  markup=True, font_size='20sp', size_hint=(0.1, 0.1),
                  pos=(500, 320))
        with im.canvas:
            Color(0, 0, 0, 0.3)
            Rectangle(pos=(450, 165), size=(300, 360))
            size_hint = (1.0, 1.0)

        # this is the button used for sign up

        buttonflight = Button(
            text='[b]Start your journey....[/b]',
            markup=True,
            color=(0, 0, 0, 1),
            size_hint=(0.38, 0.1),
            pos=(450, 100),
            background_color=(255, 255, 255, 1),
            )

        # button used to go back

        buttongoback = Button(text='Go Back', size_hint=(0.2, 0.08),
                              pos=(10, 525), background_color=(0, 0, 0,
                              0.3))

        f2.add_widget(f1)
        f1.add_widget(label1)

        f1.add_widget(buttonflight)
        f1.add_widget(buttongoback)

        buttonflight.bind(on_press=self.flightchanger)
        buttongoback.bind(on_press=self.gobackchanger)

        self.add_widget(f2)

    def gobackchanger(self, *args):
        self.manager.current = 'screen2'

    def flightchanger(self, *args):
        self.manager.current = 'flightmain'


# this is the screen that shows up when we want to book the flight

class flightMain(Screen):

    def on_r2_active(self, r2, value):
        if value:
            global arrl
            global arrin
            global return_true
            return_true = 1
            arrl = Label(text='[b]Arrival[/b]', markup=True, pos=(90,
                         -30), font_size=17)
            arrin = TextInput(hint_text='dd/mm/yyyy', size_hint=(0.3,
                              0.05), pos=(465, 220), multiline=False)
            self.add_widget(arrl)
            self.add_widget(arrin)

    def on_r1_active(self, r1, value):
        if value:
            global arrl
            global arrin
            global return_true
            return_true = 0
            self.remove_widget(arrl)
            self.remove_widget(arrin)

    def __init__(self, **kwargs):
        super(flightMain, self).__init__(**kwargs)
        global adropdown
        global cdropdown
        global idropdown
        global return_true
        im = AsyncImage(source='flightmainpage.jpg', size_hint=(1.9,
                        1.0), pos_hint={'x': -.5, 'y': 0})

                # source = "https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2017/08/24/104670887-VacationExplainsTHUMBWEB.1910x1000.jpg",
                # source = "https://media.cntraveler.com/photos/5972359c1a44557ccdfd9a25/master/w_775,c_limit/Glacier-Bay-National-Park-GettyImages-486433496.jpg",
                # source = "https://cdn.theculturetrip.com/wp-content/uploads/2015/01/shutterstock_316848560.jpg",

        h1 = Label(text='[b]Search Flights[/b]', markup=True,
                   pos=(-235, 260), font_size=50, background_color=(1,
                   1, 1, 1))
        h2 = Label(text='[b]Start your journey[/b]', markup=True,
                   pos=(-295, 210), font_size=25, background_color=(1,
                   1, 1, 1))
        f = FloatLayout()

        r1 = CheckBox(active=True, size=(25, 25), group='group1',
                      pos=(100, 417), allow_no_selection=False)
        r2 = CheckBox(active=False, size=(25, 25), group='group1',
                      pos=(457, 417), allow_no_selection=False)

        r1.bind(active=self.on_r1_active)
        r2.bind(active=self.on_r2_active)

    # f1 = FloatLayout(pos_hint={'top': 0.9},size_hint=(1.0,1.0))
    # this is used to give a canvas transparent color to the screen

        rt1 = Label(text='[b]One Way[/b]', markup=True, pos=(-245,
                    129), color=(1, 1, 1, 1))
        rt2 = Label(text='[b]Round trip[/b]', markup=True, pos=(115,
                    129))

        im.add_widget(r1)
        im.add_widget(r2)

        with im.canvas:
            Color(0, 0, 0, 0.3)
            Rectangle(pos=(55, 89), size=(700, 400))
            size_hint = (1.0, 1.0)

        global fromin
        global toin
        global depin

        froml = Label(text='[b]From[/b]', markup=True, pos=(-285, 70),
                      font_size=17)
        fromin = TextInput(hint_text='Write location', markup=True,
                           size_hint=(0.3, 0.05), pos=(95, 320),
                           multiline=False)

        tol = Label(text='[b]To[/b]', markup=True, pos=(75, 70),
                    font_size=17)
        toin = TextInput(hint_text='Write location', size_hint=(0.3,
                         0.05), pos=(465, 320), multiline=False)

        depl = Label(text='[b]Depart on[/b]', markup=True, pos=(-268,
                     -30), font_size=17)
        depin = TextInput(hint_text='dd/mm/yyyy', size_hint=(0.3,
                          0.05), pos=(95, 220), multiline=False)

        adultl = Label(text='[b]Adults[/b]', markup=True, pos=(-280,
                       -105))
        childl = Label(text='[b]Children[/b]', markup=True, pos=(-165,
                       -105))
        infantl = Label(text='[b]Infant[/b]', markup=True, pos=(-65,
                        -105))

        adropdown = DropDown(pos=(0, 110))
        cdropdown = DropDown(pos=(40, 110))
        idropdown = DropDown(pos=(200, 110))

        searchbutton = Button(background_color=(0, 0, 0.7, 0.8),
                              text='Search Flights', font_size=25,
                              pos=(500, 110), size_hint=(0.25, 0.1))
        searchbutton.bind(on_press=self.searchchanger)

         # button used to go back

        buttongoback = Button(text='Go Back', size_hint=(0.2, 0.08),
                              pos=(650, 550), background_color=(0, 0,
                              0, 0.1))

        buttongoback.bind(on_press=self.gobackchanger)
        for index in range(1, 9):
            btn = Button(text='Value %d' % index, size_hint_y=None,
                         height=17)
            btn.bind(on_release=lambda btn: adropdown.select(btn.text))
            adropdown.add_widget(btn)

        for index in range(9):
            btn = Button(text='Value %d' % index, size_hint_y=None,
                         height=17)
            btn.bind(on_release=lambda btn: cdropdown.select(btn.text))
            cdropdown.add_widget(btn)

        for index in range(4):
            btn = Button(text='Value %d' % index, size_hint_y=None,
                         height=17)
            btn.bind(on_release=lambda btn: idropdown.select(btn.text))
            idropdown.add_widget(btn)

        global mainadropdown
        mainadropdown = Button(text='Select', size_hint=(0.1, 0.05),
                               pos=(95, 150))
        mainadropdown.bind(on_release=adropdown.open)

        adropdown.bind(on_select=lambda instance1, x: \
                       setattr(mainadropdown, 'text', x))

        global maincdropdown
        maincdropdown = Button(text='Select', size_hint=(0.1, 0.05),
                               pos=(205, 150))
        maincdropdown.bind(on_release=cdropdown.open)

        cdropdown.bind(on_select=lambda instance2, x: \
                       setattr(maincdropdown, 'text', x))

        global mainidropdown
        mainidropdown = Button(text='Select', size_hint=(0.1, 0.05),
                               pos=(315, 150))

        mainidropdown.bind(on_release=idropdown.open)
        idropdown.bind(on_select=lambda instance3, x: \
                       setattr(mainidropdown, 'text', x))

        f.add_widget(im)
        f.add_widget(h1)
        f.add_widget(h2)

        f.add_widget(rt1)
        f.add_widget(rt2)

        f.add_widget(froml)
        f.add_widget(fromin)
        f.add_widget(tol)
        f.add_widget(toin)
        f.add_widget(depl)
        f.add_widget(depin)
        f.add_widget(adultl)
        f.add_widget(childl)
        f.add_widget(infantl)
        f.add_widget(mainadropdown)
        f.add_widget(maincdropdown)
        f.add_widget(mainidropdown)
        f.add_widget(searchbutton)
        f.add_widget(buttongoback)
        self.add_widget(f)

    def gobackchanger(self, *args):
        fromin.hint_text = 'Write Location'
        toin.hint_text = 'Write Location'
        depin.hint_text = 'Depart on'
        self.manager.current = 'optionpage'

    def searchchanger(self, *args):
        global fromin
        global toin
        global depin
        global total_persons
        print '\n', fromin.text, '\n'

        total_persons = 0
        if mainadropdown.text != 'Select':
            total_persons += int(mainadropdown.text[-1])
        if maincdropdown.text != 'Select':
            total_persons += int(maincdropdown.text[-1])
        if mainidropdown.text != 'Select':
            total_persons += int(mainidropdown.text[-1])

        if mainadropdown.text == 'Select' or fromin.text.isspace() \
            == True or fromin.text == '' or toin.text == '' \
            or toin.text.isspace() == True or fromin.text.isdigit() \
            == True or toin.text.isdigit() == True \
            or depin.text.isspace() == True or depin.text == '':
            fromin.hint_text = 'Enter valid choice'
            fromin.hint_text_color = (1, 0, 0, 0.7)

            toin.hint_text = 'Enter valid choice'
            toin.hint_text_color = (1, 0, 0, 0.7)

            depin.hint_text = 'Enter valid choice'
            depin.hint_text_color = (1, 0, 0, 0.7)
            self.manager.current = 'flightmain'
        else:
            fromin.hint_text = 'Write Location'
            toin.hint_text = 'Write Location'
            depin.hint_text = 'Depart on'
            mainfunc()
            enter_names.build()
            self.manager.current = 'enter_names'


# This page displays the results of the search options

class enter_Names(Screen):

    def build(self, **kwargs):
        global total_persons
        super(enter_Names, self).__init__(**kwargs)
        blayout = BoxLayout(orientation='vertical')
        layout1 = StackLayout(orientation='lr-bt')
        flayout = FloatLayout()
        backim = AsyncImage(source='enterpage.jpg',
                            pos_hint={'center_x': .5, 'center_y': .5},
                            size_hint=(1.5, 1.1))
        flayout.add_widget(backim)

        # another child of layout1 and this is the scrollview which will have a custom draggable scrollbar

        scrlv = ScrollView(size_hint=(0.9, 1))

        # the last child of layout1 and this will act as the draggable scrollbar

        s = Slider(
            min=0,
            max=1,
            value=25,
            orientation='vertical',
            step=0.01,
            size_hint=(0.1, 1),
            )

        scrlv.bind(scroll_y=partial(self.slider_change, s))

        # what this does is, whenever the slider is dragged, it scrolls the previously added scrollview by the same amount the slider is dragged

        s.bind(value=partial(self.scroll_change, scrlv))

        layout2 = BoxLayout(orientation='vertical', size_hint_y=None)
        layout2.bind(minimum_height=layout2.setter('height'))

        # layout2.setter('height')
        # this calls the main function for finding all the existing paths in the graph

        for i in range(1, total_persons + 1):
            reclayout = RelativeLayout(size_hint_y=None, height=85,
                    size_hint_x=.5)
            global names_objects_list
            name_label = Label(text='[b]Passenger %d[/b]: ' % i,
                               markup=True, font_size=18, pos=(-70, -2))
            name_input = TextInput(hint_text='Enter name',
                                   size_hint=(0.9, .5),
                                   multiline=False, pos=(380, 16))
            names_objects_list.append(name_input)

            with reclayout.canvas:
                Color(0, 0, 0, .5)
                Rectangle(pos=(40, 0), size=(730, 75))
                reclayout.add_widget(name_label)
                reclayout.add_widget(name_input)

                layout2.add_widget(reclayout)
        scrlv.add_widget(layout2)
        layout1.add_widget(scrlv)
        layout1.add_widget(s)
        buttongoback = Button(text='Go Back', size_hint=(0.2, 0.1),
                              pos=(10, 525))

        buttongoback.bind(on_press=self.gobackchanger)

        # buttongoback

        h1 = Label(
            text='Enter passenger names',
            font_size=35,
            size_hint=(1, 0.1),
            markup=True,
            halign='left',
            color=(0, 0, 0, .5),
            )
        h1.bind(size=h1.setter('text_size'))
        blayout.add_widget(h1)
        blayout.add_widget(layout1)
        rt2 = Button(text='[b]Next Page[/b]', size_hint=(0.2, 0.06),
                     markup=True, pos=(580, 555), background_color=(1,
                     1, 1, 0.8))

        buttongoback = Button(text='[b]Go Back[/b]', size_hint=(0.2,
                              0.06), pos=(400, 555), markup=True,
                              background_color=(1, 1, 1, 0.8))

        buttongoback.bind(on_press=self.gobackchanger)

        rt2.bind(on_press=self.toscreenmatrix)

        flayout.add_widget(rt2)
        flayout.add_widget(buttongoback)

        flayout.add_widget(blayout)
        self.add_widget(flayout)

    # this is for the next button to go the seat matrix page..

    def toscreenmatrix(self, *args):
        flag = 0
        for i in names_objects_list:
            if i.text.isdigit() == True or i.text == '' \
                or i.text.isspace() == True:
                i.hint_text = 'Please enter a valid name'
                i.hint_text_color = (1, 0, 0, 0.7)
                flag = 1

        # the case when all details are filled and are valid

        if flag == 0:
            for i in names_objects_list:
                names_list.append(i.text)
                i.hint_text = ''
            searchpage.build()
            self.manager.current = 'searchpage'
        else:
            flag = 0
            self.manager.current = 'enter_names'

    def scroll_change(
        self,
        scrlv,
        instance,
        value,
        ):

        scrlv.scroll_y = value

    def slider_change(
        self,
        s,
        instance,
        value,
        ):

        if value >= 0:
            s.value = value

    def gobackchanger(self, *args):
        for i in names_objects_list:
            i.hint_text = ''

        global names_list
        names_list = []
        self.manager.current = 'flightmain'


# this is the page that displays the results of the search entered by the user in the previous page

class searchPage(Screen):

    def build(self, **kwargs):
        global return_true
        super(searchPage, self).__init__(**kwargs)
        blayout = BoxLayout(orientation='vertical')
        layout1 = StackLayout(orientation='lr-bt')
        flayout = FloatLayout()
        backim = AsyncImage(source='mountainbackground.jpg',
                            pos_hint={'center_x': .5, 'center_y': .5},
                            size_hint=(1.5, 1.1))
        flayout.add_widget(backim)

        # another child of layout1 and this is the scrollview which will have a custom draggable scrollbar

        scrlv = ScrollView(size_hint=(0.9, 1))

        # the last child of layout1 and this will act as the draggable scrollbar

        s = Slider(
            min=0,
            max=1,
            value=25,
            orientation='vertical',
            step=0.001,
            size_hint=(0.1, 1),
            )

        scrlv.bind(scroll_y=partial(self.slider_change, s))

        # what this does is, whenever the slider is dragged, it scrolls the previously added scrollview by the same amount the slider is dragged

        s.bind(value=partial(self.scroll_change, scrlv))

        layout2 = BoxLayout(orientation='vertical', size_hint_y=None)
        layout2.bind(minimum_height=layout2.setter('height'))

        # layout2.setter('height')
        # this calls the main function for finding all the existing paths in the graph

        print len(all_comb)

        if return_true == 1:
            for i in range(1, len(all_comb) + 1):  # +1
                for j in range(1, len(return_all_comb) + 1):  #  +1
                    reclayout = RelativeLayout(size_hint_y=None,
                            height=185, size_hint_x=1)

                    # btn = Label(text=str(i), font_size=12,pos = (-100,20))

                    # -------------------Departure Record starts here-----------------------------

                    current_date = depin.text
                    for jj in range(0, len(all_comb[i - 1][0])):
                        if all_comb[i - 1][0][jj].isalpha() == False:
                            indexno = jj
                            indexpath = jj - 1
                            indexcomp = jj + 1
                            break
                    path0 = (all_comb[i - 1][0])[0:indexpath + 1]
                    curr_nodeobject = g.search_vertex(path0)

                    # this part is used to find out the index of the plane number and the company name

                    noofarrows = 0
                    for iii in printpath[i - 1]:
                        if iii == '-':
                            noofarrows = noofarrows + 1

                    # this loop searches for the plane object that corresponds to the start time root

                    for ii in g.search_vertex(path0).plane_array:
                        if ii.plane_no == int(all_comb[i
                                - 1][0][indexno]) and ii.company_name \
                            == (all_comb[i
                                - 1][0])[indexcomp:len(all_comb[i
                                - 1][0])]:

                            break

                    start_time_list = ii.return_time(current_date,
                            curr_nodeobject, g)

                    start_time = start_time_list[0]
                    end_time = start_time \
                        + datetime.timedelta(minutes=noofarrows * 60)

                    labelcontendpath = Label(text=printpath[i - 1],
                            font_size='12sp', pos=(-150, 0))
                    labelcontendstarttime = Label(text=str(start_time),
                            font_size='15sp', pos=(-150, 20))
                    labelcontendendtime = Label(text=str(end_time),
                            font_size='15sp', pos=(50, 20))
                    stopslabel = Label(text=str(noofarrows - 1)
                            + ' Stops', font_size='12sp', pos=(255, 0))
                    durationlabel = Label(text=str(end_time
                            - start_time), font_size='15sp', pos=(255,
                            20))
                    recim = AsyncImage(source='emirates-squarelogo.png'
                            , pos=(-200, 5), size_hint=(0.8, 0.8),
                            keep_ratio=True)  # allow_stretch = True,

                    # -------------------Arrival Record starts here-----------------------------

                    return_date = arrin.text
                    for jj in range(0, len(return_all_comb[j - 1][0])):
                        if return_all_comb[j - 1][0][jj].isalpha() \
                            == False:
                            return_indexno = jj
                            return_indexpath = jj - 1
                            return_indexcomp = jj + 1
                            break
                    path0 = (return_all_comb[j
                             - 1][0])[0:return_indexpath + 1]
                    curr_nodeobject = g.search_vertex(path0)

                    # this part is used to find out the index of the plane number and the company name

                    return_noofarrows = 0
                    for iii in return_printpath[j - 1]:
                        if iii == '-':
                            return_noofarrows = return_noofarrows + 1

                    # this loop searches for the plane object that corresponds to the start time root

                    for ii in g.search_vertex(path0).plane_array:
                        if ii.plane_no == int(return_all_comb[j
                                - 1][0][return_indexno]) \
                            and ii.company_name == (return_all_comb[j
                                - 1][0])[indexcomp:len(return_all_comb[j
                                - 1][0])]:

                            break

                    return_time_list = ii.return_time(return_date,
                            curr_nodeobject, g)

                    return_start_time = return_time_list[0]  # start_time,end_time,noofarrows,printpath
                    return_end_time = return_start_time \
                        + datetime.timedelta(minutes=return_noofarrows
                            * 60)

                    # -----------------departure part------------------------------

                    labelcontendpath = Label(text=printpath[i - 1],
                            font_size='12sp', pos=(-150, 45))
                    labelcontendstarttime = Label(text=str(start_time),
                            font_size='15sp', pos=(-150, 65))
                    labelcontendendtime = Label(text=str(end_time),
                            font_size='15sp', pos=(50, 65))
                    stopslabel = Label(text=str(noofarrows - 1)
                            + ' Stops', font_size='12sp', pos=(255, 45))
                    durationlabel = Label(text=str(end_time
                            - start_time), font_size='15sp', pos=(255,
                            65))
                    choosebtn = Button(text='Book', size_hint=(0.2,
                            0.18), pos=(550, 5), background_color=(0, 1,
                            0, 0.7))
                    choosebtn.bind(on_press=partial(self.flight_chosen,
                                   i, j))

                    
                    # -----------------Return part--------------------------

                    return_labelcontendpath = \
                        Label(text=return_printpath[j - 1],
                              font_size='12sp', pos=(-150, -40))
                    return_labelcontendstarttime = \
                        Label(text=str(return_start_time),
                              font_size='15sp', pos=(-150, -20))
                    return_labelcontendendtime = \
                        Label(text=str(return_end_time),
                              font_size='15sp', pos=(50, -20))
                    return_stopslabel = \
                        Label(text=str(return_noofarrows - 1) + ' Stops'
                              , font_size='12sp', pos=(255, -40))
                    return_durationlabel = \
                        Label(text=str(return_end_time
                              - return_start_time), font_size='15sp',
                              pos=(255, -20))

                    recim = AsyncImage(source='emirates-squarelogo.png'
                            , pos=(-65, 92), size_hint=(0.43, 0.43),
                            keep_ratio=False)  # allow_stretch = True,
                    recim1 = AsyncImage(source='emirates-squarelogo.png'
                            , pos=(-65, 6), size_hint=(0.43, 0.43),
                            keep_ratio=False)  # allow_stretch = True,

                    with reclayout.canvas:
                        Color(0, 0, 0, 0.6)
                        Rectangle(pos=(40, 0), size=(730, 180))
                        reclayout.add_widget(recim)
                        reclayout.add_widget(recim1)
                        reclayout.add_widget(labelcontendpath)
                        reclayout.add_widget(labelcontendstarttime)
                        reclayout.add_widget(labelcontendendtime)
                        reclayout.add_widget(stopslabel)
                        reclayout.add_widget(durationlabel)

                        reclayout.add_widget(return_labelcontendpath)
                        reclayout.add_widget(return_labelcontendstarttime)
                        reclayout.add_widget(return_labelcontendendtime)
                        reclayout.add_widget(return_stopslabel)
                        reclayout.add_widget(return_durationlabel)
                        reclayout.add_widget(choosebtn)

                        layout2.add_widget(reclayout)
            scrlv.add_widget(layout2)
            layout1.add_widget(scrlv)
            layout1.add_widget(s)
            h1 = Label(
                text=str(len(all_comb) * len(return_all_comb))
                    + ' results found...',
                font_size=40,
                size_hint=(1, 0.1),
                markup=True,
                halign='left',
                color=(0, 0, 0, .5),
                )
            h1.bind(size=h1.setter('text_size'))
            blayout.add_widget(h1)
        else:

            for i in range(1, len(all_comb) + 1):
                reclayout = RelativeLayout(size_hint_y=None,
                        height=100, size_hint_x=1)

            # btn = Label(text=str(i), font_size=12,pos = (-100,20))

                current_date = depin.text
                for jj in range(0, len(all_comb[i - 1][0])):
                    if all_comb[i - 1][0][jj].isalpha() == False:
                        indexno = jj
                        indexpath = jj - 1
                        indexcomp = jj + 1
                        break
                path0 = (all_comb[i - 1][0])[0:indexpath + 1]
                curr_nodeobject = g.search_vertex(path0)

                # this part is used to find out the index of the plane number and the company name

                noofarrows = 0
                for iii in printpath[i - 1]:
                    if iii == '-':
                        noofarrows = noofarrows + 1

                # this loop searches for the plane object that corresponds to the start time root

                for ii in g.search_vertex(path0).plane_array:
                    if ii.plane_no == int(all_comb[i - 1][0][indexno]) \
                        and ii.company_name == (all_comb[i
                            - 1][0])[indexcomp:len(all_comb[i - 1][0])]:

                        break

                start_time_list = ii.return_time(current_date,
                        curr_nodeobject, g)

                start_time = start_time_list[0]
                end_time = start_time \
                    + datetime.timedelta(minutes=noofarrows * 60)

                labelcontendpath = Label(text=printpath[i - 1],
                        font_size='12sp', pos=(-150, 0))
                labelcontendstarttime = Label(text=str(start_time),
                        font_size='15sp', pos=(-150, 20))
                labelcontendendtime = Label(text=str(end_time),
                        font_size='15sp', pos=(50, 20))
                stopslabel = Label(text=str(noofarrows - 1) + ' Stops',
                                   font_size='12sp', pos=(255, 0))
                durationlabel = Label(text=str(end_time - start_time),
                        font_size='15sp', pos=(255, 20))
                choosebtn = Button(text='Book', size_hint=(0.2, 0.3),
                                   pos=(550, 5), background_color=(0,
                                   1, 0, 0.7))
                j = 1
                choosebtn.bind(on_press=partial(self.flight_chosen, i,
                               j))
                recim = AsyncImage(source='emirates-squarelogo.png',
                                   pos=(-200, 5), size_hint=(0.8, 0.8),
                                   keep_ratio=True)  # allow_stretch = True,

                with reclayout.canvas:
                    Color(0, 0, 0, 0.6)
                    Rectangle(pos=(40, 0), size=(730, 90))
                    reclayout.add_widget(recim)
                    reclayout.add_widget(labelcontendpath)
                    reclayout.add_widget(labelcontendstarttime)
                    reclayout.add_widget(labelcontendendtime)
                    reclayout.add_widget(stopslabel)
                    reclayout.add_widget(durationlabel)
                    reclayout.add_widget(choosebtn)

                    layout2.add_widget(reclayout)
            scrlv.add_widget(layout2)
            layout1.add_widget(scrlv)
            layout1.add_widget(s)
            h1 = Label(
                text=str(len(all_comb)) + ' results found...',
                font_size=40,
                size_hint=(1, 0.1),
                markup=True,
                halign='left',
                color=(0, 0, 0, .5),
                )
            h1.bind(size=h1.setter('text_size'))
            blayout.add_widget(h1)

        buttongoback = Button(text='Go Back', size_hint=(0.2, 0.1),
                              pos=(10, 525))

        buttongoback.bind(on_press=self.gobackchanger)

        # buttongoback

        blayout.add_widget(layout1)
        rt2 = Button(text='[b]Next Page[/b]', size_hint=(0.2, 0.06),
                     markup=True, pos=(580, 555), background_color=(1,
                     1, 1, 0.8))

        buttongoback = Button(text='[b]Go Back[/b]', size_hint=(0.2,
                              0.06), pos=(400, 555), markup=True,
                              background_color=(1, 1, 1, 0.8))

        buttongoback.bind(on_press=self.gobackchanger)

        rt2.bind(on_press=self.toscreenmatrix)

        flayout.add_widget(rt2)
        flayout.add_widget(buttongoback)

        flayout.add_widget(blayout)
        self.add_widget(flayout)

    # this is for the next button to go the seat matrix page..

    def toscreenmatrix(self, *args):
        self.manager.current = 'seatmatrix'

    def scroll_change(
        self,
        scrlv,
        instance,
        value,
        ):

        scrlv.scroll_y = value

    def slider_change(
        self,
        s,
        instance,
        value,
        ):

        if value >= 0:
            s.value = value

    def gobackchanger(self, *args):
        global names_objects_list
        global names_list
        names_objects_list = []
        names_list = []
        self.manager.current = 'flightmain'

    def flight_chosen(
        self,
        i,
        j,
        *args
        ):
        global entry_index
        global g
        global unprocessed_list
        global countseatmatrix
        global return_unprocessed_list
        global return_countseatmatrix
        global return_entry_index

        if return_true == 0:

            entry_index = i - 1
            unprocessed_list = (printflightmain[entry_index])[:]
            print unprocessed_list

            for i in range(len(unprocessed_list)):
                unprocessed_list[i] = int(unprocessed_list[i][2])
            print unprocessed_list

            for i in range(len(unprocessed_list)):
                l = printpath[entry_index].split('->')
                node = g.search_vertex(l[i])
                for j in node.plane_array:
                    if j.plane_no == unprocessed_list[i]:  # unprocessed_list holds the list of plane objects in order
                        unprocessed_list[i] = j

            countseatmatrix = 0

            for i in unprocessed_list:
                print i.plane_no, i.company_name, '\n'
            seatmatrix.build()
            self.manager.current = 'seatmatrix'
        else:

            print 'i = ', i, '\n'
            print 'j = ', j, '\n'
            print 'i*j = ', i * j
            entry_index = i - 1
            return_entry_index = j - 1

            unprocessed_list = (printflightmain[entry_index])[:]
            print unprocessed_list
            print return_unprocessed_list
            for i in range(len(unprocessed_list)):
                unprocessed_list[i] = int(unprocessed_list[i][2])
            print unprocessed_list

            for i in range(len(unprocessed_list)):
                l = printpath[entry_index].split('->')
                node = g.search_vertex(l[i])
                for j in node.plane_array:
                    if j.plane_no == unprocessed_list[i]:  # unprocessed_list holds the list of plane objects in order
                        unprocessed_list[i] = j

            countseatmatrix = 0

            for i in unprocessed_list:
                print i.plane_no, i.company_name, '\n'

        # Return part

            return_unprocessed_list = \
                (return_printflightmain[return_entry_index])[:]
            print return_unprocessed_list
            for i in range(len(return_unprocessed_list)):
                return_unprocessed_list[i] = \
                    int(return_unprocessed_list[i][2])
            print return_unprocessed_list

            for i in range(len(return_unprocessed_list)):
                l = return_printpath[return_entry_index].split('->')
                node = g.search_vertex(l[i])
                for j in node.plane_array:
                    if j.plane_no == return_unprocessed_list[i]:  # unprocessed_list holds the list of plane objects in order
                        return_unprocessed_list[i] = j

            return_countseatmatrix = 0

            for i in return_unprocessed_list:
                print i.plane_no, i.company_name, '\n'
            seatmatrix.build()
            self.manager.current = 'seatmatrix'


# this page is used to display the seat matrix of the flights sequence found out as a result of the search operation from the previous page.

class SeatMatrix(Screen):

    def build(self, **kwargs):
        global countseatmatrix
        global g
        global unprocessed_list
        global return_countseatmatrix
        global return_unprocessed_list
        global chosen_seats_count
        global return_chosen_seats_count
        global return_entry_index

        super(SeatMatrix, self).__init__(**kwargs)

        chosen_seats_count = 0
        return_chosen_seats_count = 0

        if return_true == 0 or deptoreturn == 0:

            f = FloatLayout()
            self.buttons = []
            backim = AsyncImage(source='seatmatrixbackground.jpg',
                                pos_hint={'center_x': .5,
                                'center_y': 0.45}, allow_stretch=True,
                                size_hint=(1.7, 1.65), keep_ratio=False)

            f.add_widget(backim)
            tempstr = 'A'
            tempint = 15
            k = 1
            l = printpath[entry_index].split('->')

            dep_date_list = depin.text.split('/')

            dep_day = int(dep_date_list[0])
            dep_month = int(dep_date_list[1])
            dep_year = int(dep_date_list[2])
            dep_hour = int(time_list[entry_index][countseatmatrix].hour)
            dep_minute = \
                int(time_list[entry_index][countseatmatrix].minute)

            dep_datetime = datetime.datetime(dep_year, dep_month,
                    dep_day, dep_hour, dep_minute)
            try:
                sm = \
                    unprocessed_list[countseatmatrix].seating_matrix[dep_datetime]
            except:
                sm = [[0 for j in range(4)] for i in range(15)]
                unprocessed_list[countseatmatrix].seating_matrix[dep_datetime] = \
                    sm

            for i in range(0, 15):
                for j in range(0, 2):
                    if sm[i][j] == 0:
                        seats = Button(background_color=(0, 0, 1, 1),
                                size_hint=(0.015, 0.02), pos=(360 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')
                    else:
                        seats = Button(background_color=(1, 0, 0, 1),
                                size_hint=(0.015, 0.02), pos=(360 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')
                    f.add_widget(seats)
                    seats.bind(on_press=self.colorchanger)
                    self.buttons.append(seats)

                    # seats[k].bind(on_press = lambda x:seatchangecolor(i))
                    # basically the next alphabet indicating the next row of the seat matrix.

                    tempstr = chr(ord(tempstr) + 1)

                for j in range(2, 4):
                    if sm[i][j] == 0:
                        seats = Button(background_color=(0, 0, 1, 1),
                                size_hint=(0.015, 0.02), pos=(362 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')
                    else:
                        seats = Button(background_color=(1, 0, 0, 1),
                                size_hint=(0.015, 0.02), pos=(362 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')

                    f.add_widget(seats)
                    self.buttons.append(seats)
                    seats.bind(on_press=self.colorchanger)
                    tempstr = chr(ord(tempstr) + 1)

                    # k = k+1

                tempint = tempint - 1
                tempstr = 'A'

            with f.canvas:
                Color(0, 0, 1, 1)
                Rectangle(pos=(510, 410), size=(25, 25))
            with f.canvas:
                Color(0, 1, 0, 1)
                Rectangle(pos=(510, 445), size=(25, 25))
            with f.canvas:
                Color(1, 0, 0, 1)
                Rectangle(pos=(510, 480), size=(25, 25))
            with f.canvas:
                Color(0, 0, 0, 0.2)
                Rectangle(pos=(500, 400), size=(250, 150))

            with f.canvas:
                Color(0, 0, 0, 0.2)
                Rectangle(pos=(30, 400), size=(273, 150))

            legendheader = Label(
                text='[b]LEGENDS[/b]',
                markup=True,
                font_size=18,
                color=(0, 0, 0, 1),
                size_hint=(0.1, 0.1),
                pos=(510, 500),
                )
            legendoccupied = Label(text='OCCUPIED', font_size=15,
                                   color=(0, 0, 0, 1), size_hint=(0.1,
                                   0.1), pos=(546, 460))
            legendchosen = Label(text='CHOSEN', font_size=15, color=(0,
                                 0, 0, 1), size_hint=(0.1, 0.1),
                                 pos=(540, 426))
            legendvacant = Label(text='VACANT', font_size=15, color=(0,
                                 0, 0, 1), size_hint=(0.1, 0.1),
                                 pos=(540, 391))
            chooseseatheader = Label(
                text='[b]Choose your seats[/b]',
                markup=True,
                font_size=20,
                color=(0, 0, 0, 1),
                size_hint=(0.1, 0.1),
                pos=(80, 501),
                )
            description1 = \
                Label(text='1. Seats marked in red are occupied ',
                      font_size=15, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(118, 461))
            description2 = \
                Label(text='2. Click on a vacant seat to select it',
                      font_size=15, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(117, 441))
            description3 = \
                Label(text='3. Click on a chosen seat to deselect it',
                      font_size=15, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(127, 421))

            flightlabel = \
                Label(text=printflightmain[entry_index][countseatmatrix],
                      font_size=35, color=(1, 1, 1, 1), pos=(0, 250))
            buttonbp = Button(text='[b]Next[/b]', markup=True,
                              size_hint=(0.2, 0.08), pos=(605, 20),
                              background_color=(0, 1, 0, 1))
            buttonbp.bind(on_press=partial(self.toboardingpass, f))
            buttonpp = Button(text='[b]Try another search[/b]',
                              markup=True, size_hint=(0.2, 0.08),
                              pos=(20, 20), background_color=(1, 0, 0,
                              1))
            buttonpp.bind(on_press=self.tosearchscreen)

            f.add_widget(legendheader)
            f.add_widget(legendoccupied)
            f.add_widget(legendchosen)
            f.add_widget(legendvacant)
            f.add_widget(chooseseatheader)
            f.add_widget(description1)
            f.add_widget(description2)
            f.add_widget(description3)
            f.add_widget(flightlabel)
            f.add_widget(buttonpp)
            f.add_widget(buttonbp)
            self.add_widget(f)
        else:

            f = FloatLayout()
            self.buttons = []
            backim = AsyncImage(source='seatmatrixbackground.jpg',
                                pos_hint={'center_x': .5,
                                'center_y': 0.45}, allow_stretch=True,
                                size_hint=(1.7, 1.65), keep_ratio=False)

            f.add_widget(backim)
            tempstr = 'A'
            tempint = 15
            k = 1

            l = return_printpath[return_entry_index].split('->')

            return_date_list = arrin.text.split('/')

            return_day = int(return_date_list[0])
            return_month = int(return_date_list[1])
            return_year = int(return_date_list[2])
            return_hour = \
                int(return_time_list[return_entry_index][return_countseatmatrix].hour)
            return_minute = \
                int(return_time_list[return_entry_index][return_countseatmatrix].minute)

            return_datetime = datetime.datetime(return_year,
                    return_month, return_day, return_hour,
                    return_minute)
            try:
                sm = \
                    return_unprocessed_list[return_countseatmatrix].seating_matrix[return_datetime]
            except:
                sm = [[0 for j in range(4)] for i in range(15)]
                return_unprocessed_list[return_countseatmatrix].seating_matrix[return_datetime] = \
                    sm

            for i in range(0, 15):
                for j in range(0, 2):
                    if sm[i][j] == 0:
                        seats = Button(background_color=(0, 0, 1, 1),
                                size_hint=(0.015, 0.02), pos=(360 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')
                    else:
                        seats = Button(background_color=(1, 0, 0, 1),
                                size_hint=(0.015, 0.02), pos=(360 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')
                    f.add_widget(seats)
                    seats.bind(on_press=self.colorchanger)
                    self.buttons.append(seats)

                    # seats[k].bind(on_press = lambda x:seatchangecolor(i))
                    # basically the next alphabet indicating the next row of the seat matrix.

                    tempstr = chr(ord(tempstr) + 1)

                for j in range(2, 4):
                    if sm[i][j] == 0:
                        seats = Button(background_color=(0, 0, 1, 1),
                                size_hint=(0.015, 0.02), pos=(362 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')
                    else:
                        seats = Button(background_color=(1, 0, 0, 1),
                                size_hint=(0.015, 0.02), pos=(362 + 22
                                * j, 180 + 22 * i), text=str(tempint)
                                + tempstr, font_size='10sp')

                    f.add_widget(seats)
                    self.buttons.append(seats)
                    seats.bind(on_press=self.colorchanger)
                    tempstr = chr(ord(tempstr) + 1)

                    # k = k+1

                tempint = tempint - 1
                tempstr = 'A'

            with f.canvas:
                Color(0, 0, 1, 1)
                Rectangle(pos=(510, 410), size=(25, 25))
            with f.canvas:
                Color(0, 1, 0, 1)
                Rectangle(pos=(510, 445), size=(25, 25))
            with f.canvas:
                Color(1, 0, 0, 1)
                Rectangle(pos=(510, 480), size=(25, 25))
            with f.canvas:
                Color(0, 0, 0, 0.2)
                Rectangle(pos=(500, 400), size=(250, 150))

            with f.canvas:
                Color(0, 0, 0, 0.2)
                Rectangle(pos=(30, 400), size=(273, 150))

            legendheader = Label(
                text='[b]LEGENDS[/b]',
                markup=True,
                font_size=18,
                color=(0, 0, 0, 1),
                size_hint=(0.1, 0.1),
                pos=(510, 500),
                )
            legendoccupied = Label(text='OCCUPIED', font_size=15,
                                   color=(0, 0, 0, 1), size_hint=(0.1,
                                   0.1), pos=(546, 460))
            legendchosen = Label(text='CHOSEN', font_size=15, color=(0,
                                 0, 0, 1), size_hint=(0.1, 0.1),
                                 pos=(540, 426))
            legendvacant = Label(text='VACANT', font_size=15, color=(0,
                                 0, 0, 1), size_hint=(0.1, 0.1),
                                 pos=(540, 391))
            chooseseatheader = Label(
                text='[b]Choose your seats[/b]',
                markup=True,
                font_size=20,
                color=(0, 0, 0, 1),
                size_hint=(0.1, 0.1),
                pos=(80, 501),
                )
            description1 = \
                Label(text='1. Seats marked in red are occupied ',
                      font_size=15, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(118, 461))
            description2 = \
                Label(text='2. Click on a vacant seat to select it',
                      font_size=15, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(117, 441))
            description3 = \
                Label(text='3. Click on a chosen seat to deselect it',
                      font_size=15, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(127, 421))

            flightlabel = \
                Label(text=return_printflightmain[return_entry_index][return_countseatmatrix],
                      font_size=35, color=(1, 1, 1, 1), pos=(0, 250))
            buttonbp = Button(text='[b]Next[/b]', markup=True,
                              size_hint=(0.2, 0.08), pos=(605, 20),
                              background_color=(0, 1, 0, 1))
            buttonbp.bind(on_press=partial(self.toboardingpass, f))
            buttonpp = Button(text='[b]Try another search[/b]',
                              markup=True, size_hint=(0.2, 0.08),
                              pos=(20, 20), background_color=(1, 0, 0,
                              1))
            buttonpp.bind(on_press=self.tosearchscreen)

            f.add_widget(legendheader)
            f.add_widget(legendoccupied)
            f.add_widget(legendchosen)
            f.add_widget(legendvacant)
            f.add_widget(chooseseatheader)
            f.add_widget(description1)
            f.add_widget(description2)
            f.add_widget(description3)
            f.add_widget(flightlabel)
            f.add_widget(buttonpp)
            f.add_widget(buttonbp)
            self.add_widget(f)

    def toboardingpass(self, f, *args):
        global countseatmatrix
        global total_persons
        global return_true
        global boardingpass
        print 'Countseatmatrix : ', countseatmatrix
        print chosen_seats
        global deptoreturn  # 0 when departure flights are shown, 1 when return flights are shown
        global return_chosen_seats
        global return_countseatmatrix
        
        print 'Return_countseatmatrix : ', return_countseatmatrix
        print return_chosen_seats

        if return_true == 0:

            try:
                if chosen_seats_count != total_persons:
                    with f.canvas:
                        Color(0, 0, 0, 0.2)
                        Rectangle(pos=(30, 370), size=(273, 20))
                    errorlabel = \
                        Label(text='Error: Choose only %d seats'
                              % total_persons, font_size=15, color=(1,
                              0, 0, 1), pos=(-270, 80))
                    f.add_widget(errorlabel)
                    return
            except:
                with f.canvas:
                    Color(0, 0, 0, 0.2)
                    Rectangle(pos=(30, 370), size=(273, 20))
                errorlabel = Label(text='Error: Choose only %d seats'
                                   % total_persons, font_size=15,
                                   color=(1, 0, 0, 1), pos=(-270, 80))
                f.add_widget(errorlabel)
                return

            countseatmatrix = countseatmatrix + 1

            if countseatmatrix == len(unprocessed_list):
                countseatmatrix = 0
                boardingpass.next()
                for i in chosen_seats:  # Iterating through the plane numbers of chosen_seats --will be ignored if chosen_seats == {}
                    for k in range(len(unprocessed_list)):  # Iterating through the plane objects of the planes involved in the trip
                        if unprocessed_list[k].plane_no == i:  # If plane numbers match
                            for s in chosen_seats[i]:  # Modify the seat matrix of the plane

                                dep_date_list = depin.text.split('/')

                                dep_day = int(dep_date_list[0])
                                dep_month = int(dep_date_list[1])
                                dep_year = int(dep_date_list[2])
                                dep_hour = \
                                    int(time_list[entry_index][k].hour)
                                dep_minute = \
                                    int(time_list[entry_index][k].minute)

                                dep_datetime = \
                                    datetime.datetime(dep_year,
                                        dep_month, dep_day, dep_hour,
                                        dep_minute)
                                if unprocessed_list[k].seating_matrix[dep_datetime][s[0]][s[1]] \
                                    == 2:
                                    unprocessed_list[k].seating_matrix[dep_datetime][s[0]][s[1]] = \
    1

                self.manager.current = 'boardingpass'
                return
            self.build()
            self.manager.current = 'seatmatrix'
        else:

            if deptoreturn == 0:

                try:

                    if chosen_seats_count != total_persons:
                        with f.canvas:
                            Color(0, 0, 0, 0.2)
                            Rectangle(pos=(30, 370), size=(273, 20))
                        errorlabel = \
                            Label(text='Error: Choose only %d seats'
                                  % total_persons, font_size=15,
                                  color=(1, 0, 0, 1), pos=(-270, 80))
                        f.add_widget(errorlabel)
                        return
                except:
                    with f.canvas:
                        Color(0, 0, 0, 0.2)
                        Rectangle(pos=(30, 370), size=(273, 20))
                    errorlabel = \
                        Label(text='Error: Choose only %d seats'
                              % total_persons, font_size=15, color=(1,
                              0, 0, 1), pos=(-270, 80))
                    f.add_widget(errorlabel)
                    return

                countseatmatrix = countseatmatrix + 1

                if countseatmatrix == len(unprocessed_list):
                    countseatmatrix = 0
                    deptoreturn = 1

                self.build()
                self.manager.current = 'seatmatrix'
            else:

                try:
                    if return_chosen_seats_count != total_persons:
                        with f.canvas:
                            Color(0, 0, 0, 0.2)
                            Rectangle(pos=(30, 370), size=(273, 20))
                        errorlabel = \
                            Label(text='Error: Choose only %d seats'
                                  % total_persons, font_size=15,
                                  color=(1, 0, 0, 1), pos=(-270, 80))
                        f.add_widget(errorlabel)
                        return
                except:
                    with f.canvas:
                        Color(0, 0, 0, 0.2)
                        Rectangle(pos=(30, 370), size=(273, 20))
                    errorlabel = \
                        Label(text='Error: Choose only %d seats'
                              % total_persons, font_size=15, color=(1,
                              0, 0, 1), pos=(-270, 80))
                    f.add_widget(errorlabel)
                    return

                return_countseatmatrix = return_countseatmatrix + 1

                if return_countseatmatrix \
                    == len(return_unprocessed_list):
                    return_countseatmatrix = 0
                    deptoreturn = 0
                    boardingpass.next()
                    for i in chosen_seats:  # Iterating through the plane numbers of chosen_seats --will be ignored if chosen_seats == {}
                        for k in range(len(unprocessed_list)):  # Iterating through the plane objects of the planes involved in the trip
                            if unprocessed_list[k].plane_no == i:  # If plane numbers match
                                for s in chosen_seats[i]:  # Modify the seat matrix of the plane

                                    dep_date_list = depin.text.split('/'
        )

                                    dep_day = int(dep_date_list[0])
                                    dep_month = int(dep_date_list[1])
                                    dep_year = int(dep_date_list[2])
                                    dep_hour = \
    int(time_list[entry_index][k].hour)
                                    dep_minute = \
    int(time_list[entry_index][k].minute)

                                    dep_datetime = \
    datetime.datetime(dep_year, dep_month, dep_day, dep_hour,
                      dep_minute)
                                    if unprocessed_list[k].seating_matrix[dep_datetime][s[0]][s[1]] \
    == 2:
                                        unprocessed_list[k].seating_matrix[dep_datetime][s[0]][s[1]] = \
    1

                    for i in return_chosen_seats:  # Iterating through the plane numbers of return_chosen_seats --will be ignored if return_chosen_seats == {}
                        for k in range(len(return_unprocessed_list)):  # Iterating through the plane objects of the planes involved in the trip
                            if return_unprocessed_list[k].plane_no == i:  # If plane numbers match
                                for s in return_chosen_seats[i]:  # Modify the seat matrix of the plane

                                    return_date_list = \
    arrin.text.split('/')

                                    return_day = \
    int(return_date_list[0])
                                    return_month = \
    int(return_date_list[1])
                                    return_year = \
    int(return_date_list[2])
                                    return_hour = \
    int(return_time_list[return_entry_index][k].hour)
                                    return_minute = \
    int(return_time_list[return_entry_index][k].minute)

                                    return_datetime = \
    datetime.datetime(return_year, return_month, return_day,
                      return_hour, return_minute)
                                    if return_unprocessed_list[k].seating_matrix[return_datetime][s[0]][s[1]] \
    == 2:
                                        return_unprocessed_list[k].seating_matrix[return_datetime][s[0]][s[1]] = \
    1
                    self.manager.current = 'boardingpass'
                    return

                self.build()
                self.manager.current = 'seatmatrix'

    def tosearchscreen(self, *args):
        global unprocessed_list
        global return_unprocessed_list
        global countseatmatrix
        global return_countseatmatrix
        global boarding_pass_page_reached
        global chosen_seats  # chosen_seats is a dictionary of the form {plane_no : [[row,column],[row,column]]}
        global return_chosen_seats
        global deptoreturn
        if boarding_pass_page_reached != 1:

            for i in chosen_seats:  # Iterating through the plane numbers of chosen_seats --will be ignored if chosen_seats == {}
                for k in range(len(unprocessed_list)):  # Iterating through the plane objects of the planes involved in the trip
                    if unprocessed_list[k].plane_no == i:  # If plane numbers match
                        for s in chosen_seats[i]:  # Modify the seat matrix of the plane

                            dep_date_list = depin.text.split('/')

                            dep_day = int(dep_date_list[0])
                            dep_month = int(dep_date_list[1])
                            dep_year = int(dep_date_list[2])
                            dep_hour = \
                                int(time_list[entry_index][k].hour)
                            dep_minute = \
                                int(time_list[entry_index][k].minute)

                            dep_datetime = datetime.datetime(dep_year,
                                    dep_month, dep_day, dep_hour,
                                    dep_minute)
                            try:
                                if unprocessed_list[k].seating_matrix[dep_datetime][s[0]][s[1]] \
                                    == 2:
                                    unprocessed_list[k].seating_matrix[dep_datetime][s[0]][s[1]] = \
    0
                            except:
                                pass

            for i in return_chosen_seats:  # Iterating through the plane numbers of return_chosen_seats --will be ignored if return_chosen_seats == {}
                for k in range(len(return_unprocessed_list)):  # Iterating through the plane objects of the planes involved in the trip
                    if return_unprocessed_list[k].plane_no == i:  # If plane numbers match
                        for s in return_chosen_seats[i]:  # Modify the seat matrix of the plane

                            return_date_list = arrin.text.split('/')

                            return_day = int(return_date_list[0])
                            return_month = int(return_date_list[1])
                            return_year = int(return_date_list[2])
                            return_hour = \
                                int(return_time_list[return_entry_index][k].hour)
                            return_minute = \
                                int(return_time_list[return_entry_index][k].minute)

                            return_datetime = \
                                datetime.datetime(return_year,
                                    return_month, return_day,
                                    return_hour, return_minute)
                            try:
                                if return_unprocessed_list[k].seating_matrix[return_datetime][s[0]][s[1]] \
                                    == 2:
                                    return_unprocessed_list[k].seating_matrix[return_datetime][s[0]][s[1]] = \
    0
                            except:
                                pass

        unprocessed_list = unprocessed_list[:]  # Before emptying the unprocessed list we have to remove the binding of unprocessed_list to g
        unprocessed_list = []
        return_unprocessed_list = return_unprocessed_list[:]
        return_unprocessed_list = []
        chosen_seats = chosen_seats.copy()
        chosen_seats = {}
        return_chosen_seats = return_chosen_seats.copy()
        return_chosen_seats = {}
        countseatmatrix = 0
        return_countseatmatrix = 0
        deptoreturn = 0
        self.manager.current = 'searchpage'

    # Currently seatchangecolor is not working : Function to change the seat color after pressing

    def colorchanger(self, *args):

        global unprocessed_list
        global chosen_seats_count
        global return_chosen_seats_count

        if deptoreturn == 0 or return_true == 0:

            dep_date_list = depin.text.split('/')

            dep_day = int(dep_date_list[0])
            dep_month = int(dep_date_list[1])
            dep_year = int(dep_date_list[2])
            dep_hour = int(time_list[entry_index][countseatmatrix].hour)
            dep_minute = \
                int(time_list[entry_index][countseatmatrix].minute)

            dep_datetime = datetime.datetime(dep_year, dep_month,
                    dep_day, dep_hour, dep_minute)

            if args[0].background_color == [0, 0, 1, 1]:  # 2 - chosen seats,1 - booked seats,0 - vacant seats
                args[0].background_color = (0, 1, 0, 1)

                unprocessed_list[countseatmatrix].seating_matrix[dep_datetime][15
                        - int(args[0].text[0:-1])][ord(args[0].text[-1])
                        - 65] = 2

                chosen_seats_count = chosen_seats_count + 1

                try:
                    chosen_seats[unprocessed_list[countseatmatrix].plane_no].append([15
                            - int(args[0].text[0:-1]),
                            ord(args[0].text[-1]) - 65])
                except:
                    chosen_seats[unprocessed_list[countseatmatrix].plane_no] = \
                        [[15 - int(args[0].text[0:-1]),
                         ord(args[0].text[-1]) - 65]]
            elif args[0].background_color == [0, 1, 0, 1]:

                args[0].background_color = (0, 0, 1, 1)

                unprocessed_list[countseatmatrix].seating_matrix[dep_datetime][15
                        - int(args[0].text[0:-1])][ord(args[0].text[-1])
                        - 65] = 0

                chosen_seats_count = chosen_seats_count - 1
                try:
                    chosen_seats[unprocessed_list[countseatmatrix].plane_no].remove([15
                            - int(args[0].text[0:-1]),
                            ord(args[0].text[-1]) - 65])
                except:
                    pass
        else:

            return_date_list = arrin.text.split('/')

            return_day = int(return_date_list[0])
            return_month = int(return_date_list[1])
            return_year = int(return_date_list[2])
            return_hour = \
                int(return_time_list[return_entry_index][return_countseatmatrix].hour)
            return_minute = \
                int(return_time_list[return_entry_index][return_countseatmatrix].minute)

            return_datetime = datetime.datetime(return_year,
                    return_month, return_day, return_hour,
                    return_minute)

            if args[0].background_color == [0, 0, 1, 1]:  # 2 - chosen seats,1 - booked seats,0 - vacant seats
                args[0].background_color = (0, 1, 0, 1)

                return_unprocessed_list[return_countseatmatrix].seating_matrix[return_datetime][15
                        - int(args[0].text[0:-1])][ord(args[0].text[-1])
                        - 65] = 2

                return_chosen_seats_count = return_chosen_seats_count \
                    + 1

                try:
                    return_chosen_seats[return_unprocessed_list[return_countseatmatrix].plane_no].append([15
                            - int(args[0].text[0:-1]),
                            ord(args[0].text[-1]) - 65])
                except:
                    return_chosen_seats[return_unprocessed_list[return_countseatmatrix].plane_no] = \
                        [[15 - int(args[0].text[0:-1]),
                         ord(args[0].text[-1]) - 65]]
            elif args[0].background_color == [0, 1, 0, 1]:

                args[0].background_color = (0, 0, 1, 1)

                return_unprocessed_list[return_countseatmatrix].seating_matrix[return_datetime][15
                        - int(args[0].text[0:-1])][ord(args[0].text[-1])
                        - 65] = 0

                return_chosen_seats_count = return_chosen_seats_count \
                    - 1

                try:
                    return_chosen_seats[return_unprocessed_list[return_countseatmatrix].plane_no].remove([15
                            - int(args[0].text[0:-1]),
                            ord(args[0].text[-1]) - 65])
                except:
                    pass


# this page is used to display the boarding pass of the flights chosen by the customer.

class BoardingPass(Screen):

    def build(self, **kwargs):
        global entry_index
        global return_entry_index
        global count
        global printpath
        global printflightmain
        global names_iterator
        global chosen_seats
        global boarding_pass_page_reached
        global return_count
        global return_printpath
        global return_printflightmain
        global return_chosen_seats
        global deptoreturn
        global return_true
        global Email_id

        super(BoardingPass, self).__init__(**kwargs)

        if return_true == 0 or deptoreturn == 0:

            f = FloatLayout()
            boarding_pass_page_reached = 1
            backim0 = AsyncImage(source='boardingpassbackground.jpg',
                                 allow_stretch=True, size_hint=(1, 2),
                                 pos=(0, -400), keep_ratio=True)  # source='https://www.123freevectors.com/wp-content/original/29190-abstract-red-beige-wave-background.jpg',
            backim = AsyncImage(source='boardingpass.png',
                                pos_hint={'center_x': .5,
                                'center_y': 0.45}, allow_stretch=True,
                                keep_ratio=True)

            half1name = Label(text=username, font_size=14, color=(0, 0,
                              0, 1), size_hint=(0.1, 0.1), pos=(20,
                              290))
            half1flight = \
                Label(text=printflightmain[entry_index][count],
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(181, 230))  # Not modified

            l = printpath[entry_index].split('->')
            half1src = Label(text=l[count], font_size=14, color=(0, 0,
                             0, 1), size_hint=(0.1, 0.1), pos=(45, 230))

            print l

            half1dest = Label(text=l[count + 1], font_size=14,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(402, 230))
            half1date = Label(text=depin.text, font_size=14, color=(0,
                              0, 0, 1), size_hint=(0.1, 0.1), pos=(25,
                              180))
            half1deptime = \
                Label(text=str(time_list[entry_index][count].hour) + ':'

                      + str(time_list[entry_index][count].minute).zfill(2),
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(181, 180))
            half1gate = Label(text='A16', font_size=25, color=(0, 0, 0,
                              1), size_hint=(0.1, 0.1), pos=(8, 125))
            if count == 0:
                boarding_time = time_list[entry_index][count] \
                    - datetime.timedelta(minutes=45)
            else:
                boarding_time = time_list[entry_index][count]
            half1boarding = Label(text=str(boarding_time.hour) + ':'
                                  + str(boarding_time.minute).zfill(2),
                                  font_size=25, color=(0, 0, 0, 1),
                                  size_hint=(0.1, 0.1), pos=(190, 125))
            half1msg1 = Label(text='Please be at the boarding',
                              font_size=11, color=(0, 0, 0, 1),
                              size_hint=(0.1, 0.1), pos=(422, 185))
            half1msg2 = Label(text='gate BEFORE %s,'
                              % (str(boarding_time.hour) + ':'
                              + str(boarding_time.minute).zfill(2)),
                              font_size=11, color=(0, 0, 0, 1),
                              size_hint=(0.1, 0.1), pos=(407, 170))
            half1msg3 = Label(text='otherwise you will not be',
                              font_size=11, color=(0, 0, 0, 1),
                              size_hint=(0.1, 0.1), pos=(420, 155))
            half1msg4 = Label(text='accepted for travel', font_size=11,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(405, 140))
            half2name = Label(text=username, font_size=14, color=(0, 0,
                              0, 1), size_hint=(0.1, 0.1), pos=(610,
                              290))
            half2src = Label(text=l[count], font_size=14, color=(0, 0,
                             0, 1), size_hint=(0.1, 0.1), pos=(590,
                             252))
            half2dest = Label(text=l[count + 1], font_size=14,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(710, 252))
            half2flight = \
                Label(text=printflightmain[entry_index][count],
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(650, 252))  # Not modified
            half2deptime = \
                Label(text=str(time_list[entry_index][count].hour) + ':'

                      + str(time_list[entry_index][count].minute).zfill(2),
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(595, 180))
            half2class = Label(text='EC', font_size=25, color=(0, 0, 0,
                               1), size_hint=(0.1, 0.1), pos=(590, 125))
            current_plane_number = unprocessed_list[count].plane_no

            print count
            print current_plane_number
            print unprocessed_list
            current_seat_list = \
                (chosen_seats[current_plane_number][0])[:]
            current_seat = str(15 - current_seat_list[0]) \
                + str(chr(current_seat_list[1] + ord('A')))
            del chosen_seats[current_plane_number][0]
            half2seat = Label(text=current_seat, font_size=25,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(686, 125))

            names_iterator += 1

            next = Button(text='[b]Next[/b]', markup=True, pos=(630,
                          10), size_hint=(0.2, 0.08),
                          background_color=(0, 0, 0, 0.3))
            next.bind(on_press=self.next)
            
            # Sending email
            
            fromaddr = 'pythonpython4444@gmail.com'

            toaddrs = Email_id

            SMTPServer = 'smtp.gmail.com'

            port = 465 #587

            login = "pythonpython4444@gmail.com"

            password = "pythonpython"
            
            text_to_send = "Boarding Pass Details\n\n" + "Name: "+ username +"\nFrom: "+ half1src.text +"\nTo: "+ half1dest.text +"\nDate: "+ half1date.text +"\nTime: "+ half1deptime.text + "\nGate: "+ half1gate.text +"\nBoarding Time: "+ half1boarding.text +"\n\nThank you for booking at Ascend..\n"
                  
                  
            msg = MIMEText(text_to_send)

            #msgtxt = "http://www.google.com"+"\n\n"+"This is a test."

            #msg.set_content(msgtxt)

            msg['Subject'] = "Test"

            msg['From'] = fromaddr

            msg['To'] = toaddrs



            server = smtplib.SMTP_SSL(SMTPServer, port) #use smtplib.SMTP() if port is 587

            #server.startssl()

            server.login(login, password)

            server.sendmail(fromaddr, toaddrs, msg.as_string())

            server.quit()


            f.add_widget(backim0)
            f.add_widget(backim)
            f.add_widget(half1name)
            f.add_widget(half1flight)
            f.add_widget(half1src)
            f.add_widget(half1dest)
            f.add_widget(half1date)
            f.add_widget(half1deptime)
            f.add_widget(half1gate)
            f.add_widget(half1boarding)
            f.add_widget(half1msg1)
            f.add_widget(half1msg2)
            f.add_widget(half1msg3)
            f.add_widget(half1msg4)
            f.add_widget(half2name)
            f.add_widget(half2src)
            f.add_widget(half2dest)
            f.add_widget(half2flight)
            f.add_widget(half2deptime)
            f.add_widget(half2class)
            f.add_widget(half2seat)
            f.add_widget(next)
            self.add_widget(f)
        else:

            f = FloatLayout()
            boarding_pass_page_reached = 1
            backim0 = AsyncImage(source='boardingpassbackground.jpg',
                                 allow_stretch=True, size_hint=(1, 2),
                                 pos=(0, -400), keep_ratio=True)  # source='https://www.123freevectors.com/wp-content/original/29190-abstract-red-beige-wave-background.jpg',
            backim = AsyncImage(source='boardingpass.png',
                                pos_hint={'center_x': .5,
                                'center_y': 0.45}, allow_stretch=True,
                                keep_ratio=True)

            half1name = Label(text=username, font_size=14, color=(0, 0,
                              0, 1), size_hint=(0.1, 0.1), pos=(20,
                              290))
            half1flight = \
                Label(text=return_printflightmain[return_entry_index][return_count],
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(181, 230))  # Not modified

            l = return_printpath[return_entry_index].split('->')
            half1src = Label(text=l[return_count], font_size=14,
                             color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                             pos=(45, 230))

            print l

            half1dest = Label(text=l[return_count + 1], font_size=14,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(402, 230))
            half1date = Label(text=arrin.text, font_size=14, color=(0,
                              0, 0, 1), size_hint=(0.1, 0.1), pos=(25,
                              180))
            half1deptime = \
                Label(text=str(return_time_list[return_entry_index][return_count].hour)
                      + ':'
                      + str(return_time_list[return_entry_index][return_count].minute).zfill(2),
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(181, 180))
            half1gate = Label(text='A16', font_size=25, color=(0, 0, 0,
                              1), size_hint=(0.1, 0.1), pos=(8, 125))
            if return_count == 0:
                boarding_time = \
                    return_time_list[return_entry_index][return_count] \
                    - datetime.timedelta(minutes=45)
            else:
                boarding_time = \
                    return_time_list[return_entry_index][return_count]
            half1boarding = Label(text=str(boarding_time.hour) + ':'
                                  + str(boarding_time.minute).zfill(2),
                                  font_size=25, color=(0, 0, 0, 1),
                                  size_hint=(0.1, 0.1), pos=(190, 125))
            half1msg1 = Label(text='Please be at the boarding',
                              font_size=11, color=(0, 0, 0, 1),
                              size_hint=(0.1, 0.1), pos=(422, 185))
            half1msg2 = Label(text='gate BEFORE %s,'
                              % (str(boarding_time.hour) + ':'
                              + str(boarding_time.minute).zfill(2)),
                              font_size=11, color=(0, 0, 0, 1),
                              size_hint=(0.1, 0.1), pos=(407, 170))
            half1msg3 = Label(text='otherwise you will not be',
                              font_size=11, color=(0, 0, 0, 1),
                              size_hint=(0.1, 0.1), pos=(420, 155))
            half1msg4 = Label(text='accepted for travel', font_size=11,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(405, 140))
            half2name = Label(text=username, font_size=14, color=(0, 0,
                              0, 1), size_hint=(0.1, 0.1), pos=(610,
                              290))
            half2src = Label(text=l[return_count], font_size=14,
                             color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                             pos=(590, 252))
            half2dest = Label(text=l[return_count + 1], font_size=14,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(710, 252))
            half2flight = \
                Label(text=return_printflightmain[return_entry_index][return_count],
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(650, 252))  # Not modified
            half2deptime = \
                Label(text=str(return_time_list[return_entry_index][return_count].hour)
                      + ':'
                      + str(return_time_list[return_entry_index][return_count].minute).zfill(2),
                      font_size=14, color=(0, 0, 0, 1), size_hint=(0.1,
                      0.1), pos=(595, 180))
            half2class = Label(text='EC', font_size=25, color=(0, 0, 0,
                               1), size_hint=(0.1, 0.1), pos=(590, 125))
            current_plane_number = \
                return_unprocessed_list[return_count].plane_no
            current_seat_list = \
                (return_chosen_seats[current_plane_number][0])[:]

            current_seat = str(15 - current_seat_list[0]) \
                + str(chr(current_seat_list[1] + ord('A')))
            del return_chosen_seats[current_plane_number][0]
            half2seat = Label(text=current_seat, font_size=25,
                              color=(0, 0, 0, 1), size_hint=(0.1, 0.1),
                              pos=(686, 125))

            next = Button(text='[b]Next[/b]', markup=True, pos=(630,
                          10), size_hint=(0.2, 0.08),
                          background_color=(0, 0, 0, 0.3))
            next.bind(on_press=self.next)
            
            # Sending email
            
            fromaddr = 'pythonpython4444@gmail.com'

            toaddrs = Email_id

            SMTPServer = 'smtp.gmail.com'

            port = 465 #587

            login = "pythonpython4444@gmail.com"

            password = "pythonpython"
            
            text_to_send = "Boarding Pass Details\n\n" + "Name: "+ username +"\nFrom: "+ half1src.text +"\nTo: "+ half1dest.text +"\nDate: "+ half1date.text +"\nTime: "+ half1deptime.text + "\nGate: "+ half1gate.text +"\nBoarding Time: "+ half1boarding.text +"\n\nThank you for booking at Ascend..\n"
                  
                  
            msg = MIMEText(text_to_send)

            #msgtxt = "http://www.google.com"+"\n\n"+"This is a test."

            #msg.set_content(msgtxt)

            msg['Subject'] = "Test"

            msg['From'] = fromaddr

            msg['To'] = toaddrs



            server = smtplib.SMTP_SSL(SMTPServer, port) #use smtplib.SMTP() if port is 587

            #server.startssl()

            server.login(login, password)

            server.sendmail(fromaddr, toaddrs, msg.as_string())

            server.quit()


            names_iterator += 1

            f.add_widget(backim0)
            f.add_widget(backim)
            f.add_widget(half1name)
            f.add_widget(half1flight)
            f.add_widget(half1src)
            f.add_widget(half1dest)
            f.add_widget(half1date)
            f.add_widget(half1deptime)
            f.add_widget(half1gate)
            f.add_widget(half1boarding)
            f.add_widget(half1msg1)
            f.add_widget(half1msg2)
            f.add_widget(half1msg3)
            f.add_widget(half1msg4)
            f.add_widget(half2name)
            f.add_widget(half2src)
            f.add_widget(half2dest)
            f.add_widget(half2flight)
            f.add_widget(half2deptime)
            f.add_widget(half2class)
            f.add_widget(half2seat)
            f.add_widget(next)
            self.add_widget(f)

    def next(self, *args):
        global count
        global return_count
        global boarding_pass_page_reached
        global entry_index
        global return_entry_index
        global chosen_seats
        global return_chosen_seats
        global printpath
        global return_printpath
        global printflightmain
        global return_printflightmain
        global all_comb
        global return_all_comb
        global time_list
        global return_time_list
        global names_iterator
        global names_list
        global username
        global names_objects_list
        global fromin
        global toin
        global depin
        global arrin
        global total_persons
        global deptoreturn
        global g

        print '\n', names_list, '\n'
        if names_iterator < len(names_list):
            username = names_list[names_iterator]
            self.build()
            self.manager.current = 'boardingpass'
        elif count < len(unprocessed_list) - 1:

            names_iterator = 0  # Random order
            count = count + 1
            username = names_list[names_iterator]
            self.build()
            self.manager.current = 'boardingpass'
        elif return_count < len(return_unprocessed_list) - 1 \
            and return_true == 1:

            deptoreturn = 1
            names_iterator = 0  # Random order
            return_count += 1
            username = names_list[names_iterator]
            self.build()
            self.manager.current = 'boardingpass'
        else:

            deptoreturn = 0
            chosen_seats = {}
            return_chosen_seats = {}
            entry_index = -1
            return_entry_index = -1
            boarding_pass_page_reached = 0
            count = 0
            return_count = -1
            printflightmain = []
            return_printflightmain = []
            all_comb = []
            return_all_comb = []
            time_list = []
            return_time_list = []
            printpath = []
            return_printpath = []
            names_list = []
            names_objects_list = []
            names_iterator = 0
            total_persons = 0
            fromin.text = ''
            toin.text = ''
            depin.text = ''
            arrin.text = ''
            mainadropdown.text = 'Select'
            maincdropdown.text = 'Select'
            mainidropdown.text = 'Select'
            #-----------------
            
            f1 = open('graph.dat', 'wb')
            pickle.dump(g,f1)
            f1.close()

        
            

            #-----------------
            self.manager.current = 'screen2'
            
            
            


# this is the main function of the application.

def mainfunc():
    global g
    global return_true
    global all_comb
    global printpath
    global printflightmain
    global time_list

    global return_all_comb
    global return_printpath
    global return_printflightmain
    global return_time_list

    s = g.search_vertex(fromin.text)
    d = g.search_vertex(toin.text)

    all_paths = printAllPaths(s, d, g)

        # print p1.return_time('2/3/2018',g.search_vertex('A'),g)
        # print p1.position_determiner(360,'2/3/2018',g)
        # print t.get_weight(all_paths[1][3].node_name)

    dep_plane_list = search_flights(all_paths, depin.text, g)

    all_comb = []

    # here i stands for all the paths in the multidimensional array

    for i in dep_plane_list:

        # here j stands for all the plane root lists
        # gives the length of the number of nodes in the path.

        lenpath = len(i)

        for j in i:
            for element in itertools.product(*j):
                all_comb.append(element[:])

                # print element
    # all comb array stores all combinations of planes to reach from the source
    # to destination.
    #
    #
    # This section of the code generates all the paths sequences that has to
    # be printed on to the screen for search results.
    # ---------------------------------------------------

    for j in all_comb:
        print j
    print '\n'

    dest = toin.text

    printpath = []
    for i in all_comb:
        tempprintpath = ''
        for j in i:
            for k in j:
                if k.isalpha() == True:
                    tempprintpath = tempprintpath + str(k)
                else:
                    tempprintpath = tempprintpath + '->'
                    break
        tempprintpath = tempprintpath + dest
        printpath.append(tempprintpath[:])
    for i in printpath:
        print i

    # ---------------------------------------------------

    # ------------This section deals with the flight id generation-----------

    print '\n'

    printflightmain = []
    for i in all_comb:
        temp2 = []
        for j in i:
            temp1 = ''
            for k in j[::-1]:
                if k.isalpha() == True:
                    temp1 = temp1 + str(k)
                else:
                    temp1 = temp1 + str(k)
                    break
            temp2.append(temp1[:])
        printflightmain.append(temp2[:])

    for j in range(0, len(printflightmain)):
        for k in range(0, len(printflightmain[j])):
            m = printflightmain[j][k]
            m = m[::-1]
            m = m + m[0]
            m = m[1:len(m)]
            printflightmain[j][k] = m

    for j in printflightmain:
        print j

    # --------This section deals with the starting times at which planes depart from each stop specified in printpath-----------#

    time_list = []
    count = 0
    for i in printpath:
        l = i.split('->')
        start_node = g.search_vertex(l[0])
        for p in start_node.plane_array:
            if p.plane_no == printflightmain[count][0][2]:
                break

        list_plane = p.return_time('1/3/2018', start_node, g)
        temp = []
        temp.append(list_plane[0])
        counter = list_plane[0]
        for k in range(1, len(l)):
            cur_node = g.search_vertex(l[k])
            counter += \
                datetime.timedelta(minutes=cur_node.get_weight(l[k
                                   - 1]))
            temp.append(counter)
        time_list.append(temp[:])
        count = count + 1

    for i in time_list:
        for j in i:
            print j.day, '/', j.hour, '/', j.minute, '\t'
        print '\n'

    if return_true == 1:
        print '''
Return
'''
        return_all_paths = printAllPaths(d, s, g)
        return_plane_list = search_flights(return_all_paths,
                arrin.text, g)

        return_all_comb = []

        # here i stands for all the paths in the multidimensional array

        for i in return_plane_list:

               # here j stands for all the plane root lists
            # gives the length of the number of nodes in the path.

            lenpath = len(i)

            for j in i:
                for element in itertools.product(*j):
                    return_all_comb.append(element[:])

                    # print element
        # all comb array stores all combinations of planes to reach from the source
        # to destination.
        #
        #
        # This section of the code generates all the paths sequences that has to
        # be printed on to the screen for search results.
        # ---------------------------------------------------

        for j in return_all_comb:
            print j
        print '\n'

        dest = fromin.text

        return_printpath = []
        for i in return_all_comb:
            tempprintpath = ''
            for j in i:
                for k in j:
                    if k.isalpha() == True:
                        tempprintpath = tempprintpath + str(k)
                    else:
                        tempprintpath = tempprintpath + '->'
                        break
            tempprintpath = tempprintpath + dest
            return_printpath.append(tempprintpath[:])
        for i in return_printpath:
            print i

        # ---------------------------------------------------

        # ------------This section deals with the flight id generation-----------

        print '\n'

        return_printflightmain = []
        for i in return_all_comb:
            temp2 = []
            for j in i:
                temp1 = ''
                for k in j[::-1]:
                    if k.isalpha() == True:
                        temp1 = temp1 + str(k)
                    else:
                        temp1 = temp1 + str(k)
                        break
                temp2.append(temp1[:])
            return_printflightmain.append(temp2[:])

        for j in range(0, len(return_printflightmain)):
            for k in range(0, len(return_printflightmain[j])):
                m = return_printflightmain[j][k]
                m = m[::-1]
                m = m + m[0]
                m = m[1:len(m)]
                return_printflightmain[j][k] = m

        for j in return_printflightmain:
            print j

        # --------This section deals with the starting times at which planes depart from each stop specified in printpath-----------#

        return_time_list = []
        count = 0
        for i in return_printpath:
            l = i.split('->')
            start_node = g.search_vertex(l[0])
            for p in start_node.plane_array:
                if p.plane_no == return_printflightmain[count][0][2]:
                    break

            list_plane = p.return_time('1/3/2018', start_node, g)
            temp = []
            temp.append(list_plane[0])
            counter = list_plane[0]
            for k in range(1, len(l)):
                cur_node = g.search_vertex(l[k])
                counter += \
                    datetime.timedelta(minutes=cur_node.get_weight(l[k
                        - 1]))
                temp.append(counter)
            return_time_list.append(temp[:])
            count = count + 1

        for i in return_time_list:
            for j in i:
                print j.day, '/', j.hour, '/', j.minute, '\t'
            print '\n'


       # --------The list is generated----------------------------------------------------------------------------------------------#

class TestApp(App):

    def build(self):

        global g
        g = graph()
        g.add_vertex('AMD')
        g.add_vertex('BNK')
        g.add_vertex('COH')
        g.add_vertex('DNK')
        g.add_vertex('EM')
        g.add_edge('AMD', 'COH', 60)
        g.add_edge('EM', 'COH', 60)
        g.add_edge('DNK', 'COH', 60)
        g.add_edge('EM', 'DNK', 60)
        g.add_edge('BNK', 'DNK', 60)
        g.add_edge('BNK', 'AMD', 60)
    
        # ------------------------------------------------------------

        g.add_edge('BNK', 'COH', 60)
        p4 = plane()
        p5 = plane()
        p6 = plane()
        p7 = plane()
        p8 = plane()
        p9 = plane()
        p4.modify_plane(
            180,
            '1/3/2018',
            ['AMD', 'BNK', 'COH'],
            4,
            'EM',
            g,
            )
        p5.modify_plane(
            180,
            '1/3/2018',
            ['AMD', 'COH'],
            5,
            'AI',
            g,
            )
        p6.modify_plane(
            180,
            '1/3/2018',
            ['DNK', 'COH'],
            6,
            'JA',
            g,
            )
        p7.modify_plane(
            180,
            '1/3/2018',
            ['BNK', 'DNK'],
            7,
            'JA',
            g,
            )
        p8.modify_plane(
            180,
            '1/3/2018',
            ['EM', 'COH'],
            8,
            'AI',
            g,
            )
        p9.modify_plane(
            240,
            '1/3/2018',
            ['AMD', 'BNK', 'DNK', 'EM', 'COH'],
            9,
            'JA',
            g,
            )

        # ------------------------------------------------------------

        p1 = plane()
        p2 = plane()
        p3 = plane()

        p1.modify_plane(
            180,
            '1/3/2018',
            ['AMD', 'BNK', 'DNK', 'COH'],
            1,
            'EM',
            g,
            )
        p2.modify_plane(
            180,
            '1/3/2018',
            ['AMD', 'BNK', 'DNK', 'EM', 'COH'],
            2,
            'AI',
            g,
            )
        p3.modify_plane(
            300,
            '1/3/2018',
            ['DNK', 'EM', 'COH'],
            3,
            'JA',
            g,
            )

        #-----------------
        f1 = open('graph.dat', 'ab+')
        f1.close()
        
        flag = 0
        try:
            f1 = open('graph.dat', 'rb+')
           
            gg = pickle.load(f1)
            flag = 1
                
        except EOFError:
            flag = 0
            pickle.dump(g,f1)
            f1.close()

        if flag == 1:
            g = gg
          

        #-----------------
        my_screenmanager = ScreenManager()
        screen1 = ScreenOne(name='screen1')
        screen2 = ScreenTwo(name='screen2')
        screenusersignup = Screenusersignup(name='screenusersignup')

        # options page is the personal account page

        optionpage = OptionPage(name='optionpage')

        # flight main page is the check box entry details page

        global flightmain
        flightmain = flightMain(name='flightmain')

        global enter_names
        enter_names = enter_Names(name='enter_names')

        # search page is the page where the results are displayed

        global searchpage
        searchpage = searchPage(name='searchpage')

        # the seatmatrix page displays the seating matrix

        global seatmatrix
        seatmatrix = SeatMatrix(name='seatmatrix')

        # this page is used to display the boarding pass

        global boardingpass
        boardingpass = BoardingPass(name='boardingpass')

        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        my_screenmanager.add_widget(screenusersignup)
        my_screenmanager.add_widget(optionpage)
        my_screenmanager.add_widget(flightmain)
        my_screenmanager.add_widget(enter_names)
        my_screenmanager.add_widget(searchpage)
        my_screenmanager.add_widget(seatmatrix)
        my_screenmanager.add_widget(boardingpass)

        return my_screenmanager
 

if __name__ == '__main__':
    TestApp().run()
