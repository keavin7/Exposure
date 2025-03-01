# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:23:44 2016

@author: Sup
"""
#Add Parent Directory For Common Server / App Interface

from kivy.support import install_twisted_reactor
install_twisted_reactor()

from zope.interface import implements, implementer, Interface

from twisted.internet import reactor
from twisted.protocols import basic
from twisted.cred import credentials
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

from kivy.loader import Loader
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import *
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition, \
                                    FadeTransition, RiseInTransition
from kivy.properties import *
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
#from kivy.garden.smaa import SMAA
from kivy.garden.navigationdrawer import NavigationDrawer

from config import *
from style import *
from maps import *
from menus import *
from login import *
from message import *
from profiles import *
#from camera import *
from social_interface import *



iphone =  {'width':320 , 'height': 568}#320 x 568

Loader.num_workers = 5

SAMPLE_IMAGE = 'https://s-media-cache-ak0.pinimg.com/originals/ec/8e/8f/ec8e8f26ee298a6c852a7b7de37bd96b.jpg'
DEFAULT_LOADING_IMAGE = os.path.join(EXP_PATH,'app','loading_apeture.png')
from kivy.loader import Loader
loadingImage = Loader.image(DEFAULT_LOADING_IMAGE)

class ProfileMenu(MenuBar):
    
    def __init__(self,app,**kwargs):
        super(ProfileMenu,self).__init__(app,**kwargs)
        
        fref = weakref.ref(self.app.friends)
        pref = weakref.ref(self.app.projects)
        
        self.app.fbind('user_id',self.bind_profile_to_id)
        
        self.profile = DetailedProfileView()
        self.messages = UserListView(ref=fref)    
        self.roles =    UserListView(ref=fref)
        self.projects = ProjectListView(ref=pref)
        self.addMenuScreenWidget('overview',self.profile,**but_opt)
        self.addMenuScreenWidget('roles',self.roles,**but_opt) 
        self.addMenuScreenWidget('projects',self.projects,**but_opt)
        self.addMenuScreenWidget('messages',self.messages,**but_opt)
        
    def bind_profile_to_id(self,inst,val):
        self.profile.primary_key = val

class ProjectsMenu(MenuBar):
    
    def __init__(self,app,**kwargs):
        super(ProjectsMenu,self).__init__(app,**kwargs)
        
        fref = weakref.ref(self.app.friends)
        pref = weakref.ref(self.app.projects)
        
        lpref = weakref.ref(self.app.local_projects)
        
        self.map = MapWidget(self)
        self.local_proj_map_layer = ProjectMapView(maps = self.map,ref=lpref)  
        
        
        for screen in ('map','nearby','your projects','make'):
            print screen
            if screen == 'map':
                self.addMenuScreenWidget(screen,self.map,**but_opt)
            elif screen == 'your projects':
                project_view = MenuTabSlider(self,size_hint=(1,1))
                for _screen in ('overview','crew chat','crew list','auditions','edit'):
                    if _screen in ('crew list','crew chat','auditioins'):
                        project_view.addMenuScreenWidget(_screen,UserListView(ref=fref))
                    else:
                        project_view.addMenuScreenWidget(_screen,ProjectListView(ref=pref))
                self.addMenuScreenWidget(screen,project_view,**but_opt)
            else:
                self.addMenuScreenWidget(screen,ProjectListView(ref=pref),**but_opt)

class CastingMenu(MenuBar):

    def __init__(self,app,**kwargs):
        super(CastingMenu,self).__init__(app,**kwargs)
        
        fref = weakref.ref(self.app.friends)
        pref = weakref.ref(self.app.projects)
        
        lpref = weakref.ref(self.app.local_users)
        
        self.map = MapWidget(self)
        self.local_user_map_layer = ProfileMapView(maps = self.map,ref=lpref)        
        
        for screen in ('map','nearby','your roles','make'):
            print screen
            if screen == 'map':
                self.addMenuScreenWidget(screen,self.map,**but_opt)
            elif screen == 'nearby':
                self.addMenuScreenWidget(screen,ProjectListView(ref=pref),**but_opt)
            elif screen == 'your roles':
                role_view = MenuTabSlider(self,size_hint=(1,1))
                for _screen in ('overview','canidates','applicants','invite'):
                    if _screen in ('canidates','applicants'):
                        role_view.addMenuScreenWidget(_screen, UserListView(ref=fref))
                    else:
                        role_view.addMenuScreenWidget(_screen,ProjectListView(ref=pref))
                self.addMenuScreenWidget(screen,role_view,**but_opt)
            else:
                self.addMenuScreenWidget(screen,UserListView(ref=fref),**but_opt)

class ExposureHomeWidget(SocialHomeWidget):
    '''Manages Creen Widgets With Application Drawer'''

    app = None
    initialized = False

    profile = ObjectProperty(None)
    projects = ObjectProperty(None)
    casting = ObjectProperty(None)
    camera = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        self.touch_accept_width=50
        super(ExposureHomeWidget,self).__init__(app,**kwargs)


    def initialize(self):
        print 'initializing'

        self.profile = ProfileMenu(self.app)
        self.projects = ProjectsMenu(self.app)
        self.casting = CastingMenu(self.app)
        #self.camera = CameraWidget()
        
        self.addMenuScreenWidget('profile',CircularIcon(source=PROFILE_ICON,**icon_opt)\
                                                     ,self.profile,**font_opts)
        self.addMenuScreenWidget('projects',CircularIcon(source=PROJECTS_ICON,**icon_opt)\
                                                    ,self.projects,**font_opts)
        self.addMenuScreenWidget('casting',CircularIcon(source=CASTING_ICON,**icon_opt)\
                                                    ,self.casting,**font_opts)
        #self.addMenuScreenWidget('camera',CircularIcon(source=CAMERA_ICON,**icon_opt)\
        #                                            ,self.camera,**font_opts)
        self.addMenuScreenWidget('',RoundedButton(text='logout',**but_opt),Widget())


    def update_on_local_users(self,instance,local_users):
        pass

    def update_on_friends(self,instance,friends):
        pass

    def checkUidThenFire(self,instance,userId):
        pass

    def edit_user_info(self,*args,**kwargs):
        print 'hey hey whats going on...(im getting edited)'





class ExposureApp(SocialApp):

    #User Private Relationships
    friends = ListProperty(None)
    projects = ListProperty(None)
    
    #User Public Relationships
    local_users = ListProperty(None)
    local_projects = ListProperty(None)
    
    def auth_handler(self, *args):
        if self.authenticated == False:
            self.loginScreenManager.current = 'login'
        else:
            self.socialWidget = ExposureHomeWidget(self)
            self.appScreen.add_widget(self.socialWidget)
            self.loginScreenManager.current = 'app'
            reactor.callLater(1,self.startUpdate)

    def setupMainScreen(self):
        Window.size = (iphone['width'],iphone['height'])
        self.loginScreenManager = ScreenManager(transition=FadeTransition())

        self.loginScreen = Screen(name = 'login')
        self.login = Login(self, LOCAL_IMAGE)
        self.loginScreen.add_widget(self.login)

        self.appScreen = Screen(name = 'app')

        self.loginScreenManager.add_widget( self.loginScreen)
        self.loginScreenManager.add_widget( self.appScreen)

        self.loginScreenManager.current = 'login'
        self.bind(authenticated = self.auth_handler)
        self.bind(social_client = self.on_social_client)
        #Kickoff
        self.auth_handler()

        return self.loginScreenManager

    def update_client(self,deffered):
        print 'updating client'
        #Pass User Id
        deffered.addCallback(self.get_user_info)
        deffered.addCallback(self.get_friends)
        deffered.addCallback(self.get_local_users)
        deffered.addCallback(self.get_local_projects)
        deffered.addCallback(self.get_projects)

    def get_user_info(self, user_id=None):
        '''load user info, defaults to self, if self will update user_dict info'''

        if user_id:
            uid = user_id
        elif self.user_id:
            uid = self.user_id
        else:
            uid = None

        if self.social_client and self.authenticated and uid:
            d = self.social_client.perspective.callRemote('get_user_info', uid)
            d.addCallback(self._cb_jsonToDict)
            if self.user_id and uid == self.user_id:
                d.addCallback( self._cb_assignUserInfo )
            return d
        else:
            return None

    def get_local_users(self, *args):
        '''Yeild Users From Server'''
        print 'get local users from {}'.format(self.user_id)
        if self.social_client and self.authenticated:
            d = self.social_client.perspective.callRemote('nearby_users',100)
            return d.addCallback(self._cb_assignLocalUsers)
        else: #Shooting Blanks
            return []
            
    def get_local_projects(self, *args):
        '''Yeild Users From Server'''
        print 'get local users from {}'.format(self.user_id)
        if self.social_client and self.authenticated:
            d = self.social_client.perspective.callRemote('nearby_projects',100)
            return d.addCallback(self._cb_assignLocalProjects)
        else: #Shooting Blanks
            return []            

    def get_friends(self, *args):
        '''Yeild Users From Server'''
        print 'get friends from {}'.format(self.user_id)
        if self.social_client and self.authenticated:
            d = self.social_client.perspective.callRemote('friend_ids')
            return d.addCallback(self._cb_assignFriends)
        else: #Shooting Blanks
            return []
            
    def get_projects(self, *args):
        '''Yeild Users From Server'''
        print 'get friends from {}'.format(self.user_id)
        if self.social_client and self.authenticated:
            d = self.social_client.perspective.callRemote('project_ids')
            return d.addCallback(self._cb_assignProjects)
        else: #Shooting Blanks
            return []            

    def _cb_assignUserInfo(self,user_dict):
        print 'assigning user info {}'.format(user_dict)
        if user_dict:
            self.user_object = user_dict
            return self.user_object

    def _cb_assignLocalUsers(self,localUsersResponse):
        print 'assigning local users {}'.format( localUsersResponse )
        if localUsersResponse:
            self.local_users = localUsersResponse
            return self.local_users
        return []
        
    def _cb_assignLocalProjects(self,localProjectResponse):
        print 'assigning local projects {}'.format( localProjectResponse )
        if localProjectResponse:
            self.local_projects = localProjectResponse
            return self.local_projects
        return []        

    def _cb_assignFriends(self,friendsList):
        print 'assigning friends {}'.format( friendsList )
        if friendsList:
            self.friends = friendsList
            return self.friends
        return []
        
    def _cb_assignProjects(self,projectList):
        print 'assigning friends {}'.format( projectList )
        if projectList:
            self.projects = projectList
            return self.friends
        return []        




if __name__ == '__main__':
    app = ExposureApp()
    app.run()