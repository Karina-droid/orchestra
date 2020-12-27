import scene
import sound
import random
import objc_util


sw = scene.get_screen_size()[0]
sh = scene.get_screen_size()[1]

piano_sounds = ['piano:A3', 'piano:C3', 'piano:C4#', 'piano:D4', 'piano:E4', 'piano:F4', 'piano:G3#']
guitar_sounds = ['8ve:8ve-beep-warmguitar', 'Electric guitar plays a minor seventh_BLASTWAVEFX_06803.mp3']
drum_sounds = ['drums:Drums_01', 'drums:Drums_04', 'drums:Drums_07', 'drums:Drums_10', 'drums:Drums_13', 'drums:Drums_16']

class ButtonNode(scene.ShapeNode):
	def __init__(self, 
	action, 
	icon, 
	sounds=None, 
	tapped=None,
	time_passed=0,
	corner_radius=8, 
	border_size=20, text='', 
	text_color='black', 
	name=f'ButtonNode', 
	bg_color='white', 
	anchor_point=(0.5, 0.5), 
	borderColor=None, 
	parent=None, 
	position=(0, 0), 
	size=(120, 45),
	enabled=True,
	animated_icon=False,
	icon_animation=None,
	*args, **kwargs):
		
		# these mainly for call to super()
		self.x, self.y = position
		self.w, self.h = size
		super().__init__(
			path=scene.ui.Path.rounded_rect(self.x, self.y, self.w, self.h, corner_radius),
			fill_color=bg_color,
			stroke_color=borderColor,
			shadow=None,
			parent=parent,
			*args, **kwargs)
			
		# Normal Properties for Instance()
		self.sounds=sounds
		self.tapped=tapped
		self.time_passed=time_passed
		self.enabled=enabled
		self.button_action=action
		self.name=name
		self.position=position
		self.size=size
		self.anchor_point=anchor_point
		
		# for border
		self.border_size=border_size
		self.borderColor=bg_color
		self.corner_radius=corner_radius
		
		#for text
		self.text=text
		self.text_color=text_color
		
		# for icon
		self.icon_animation=icon_animation
		self.animated_icon=animated_icon
		self.icon=self._init_textures(icon)
		
		# Container to hold each component. 
		# is just a dict version of self.children but specific.
		self.components=dict({'icon':None, 'label':None})
		
		self._setup(self.icon, self.components)
		
	# Type Check to make sure img is a string or ui.Image
	def _init_textures(self, img):
		if type(img) == str or type(img) == scene.ui.Image:
			return scene.Texture(img)
		else:
			return None
			
	# setup our Components
	def _setup(self, i, c):
		if self.icon:
			# button picture..
			c['icon']=scene.SpriteNode(
				texture=i,
				size=scene.Size(self.size[1]/10*8, self.size[1]/10*8),
				position=scene.Point(0 , 0),
				anchor_point=(0.5, 0.5),
				parent=self,
				z_position=10)
				
		if self.text:
			#button text
			c['label']=scene.LabelNode(
				text=self.text,
				color=self.text_color,
				position=scene.Point(0, 0),
				parent=self,
				anchor_point=(0.5, 0.5), 
				z_position=9)
				
	# called when you tap the button
	def Button_Tapped(self):
		if self.components['icon']:
			if self.animated_icon and self.icon_animation:
				self.components['icon'].run_action(self.icon_animation())
		if self.enabled:
			self.button_action(self)

# custom action
def my_button_action(sender):
	sender.tapped = True
	sender.time_passed = 0
	play = random.choice(sender.sounds)
	sound.play_effect(play)
	return


def Animation_Shake(duration=1.5):
	action_list=[]
	action_list.append(
			scene.Action.rotate_to(0.25, duration/10/2))
	action_list.append(
			scene.Action.sequence(
				scene.Action.rotate_to(-0.5, duration/50),
				scene.Action.rotate_to(0.5, duration/50)))
	action_list.append(
			scene.Action.group(
				scene.Action.scale_to(1.0, duration/10/2),
				scene.Action.rotate_to(0.0, duration/10/2)))
	return scene.Action.sequence(action_list)


def Animation_Pulse(duration=1.5):
	action_list=[]
	action_list.append(
			scene.Action.sequence(
				scene.Action.scale_to(1.2, duration/10/2),
				scene.Action.scale_to(0.5, duration/10/2)))
	action_list.append(
			scene.Action.scale_to(1.2, duration/50))
	action_list.append(
			scene.Action.group(
				scene.Action.scale_to(1.0, duration/10/2)))

	return scene.Action.sequence(action_list)

def Animation_Jump(duration=1.5):
	action_list=[]
	action_list.append(
			scene.Action.sequence(
				scene.Action.move_by(0, 20, duration/20),
				scene.Action.move_to(0, 0, duration/20)))

	return scene.Action.sequence(action_list)

class Main(scene.Scene):
	def setup(self):
		self.view.multitouch_enabled
		self.buttons=list([])
		self.background_color='white'
		
		self.guitar=ButtonNode(size=scene.Size(160, 112), icon='emj:Guitar',
							parent=self, action=my_button_action, sounds=guitar_sounds,
							position=scene.Point(sw/6*1.5, sh/3), animated_icon=True,
							icon_animation=Animation_Shake)
		self.buttons.append(self.guitar)
		
		self.drum=ButtonNode(size=scene.Size(200, 112), icon='IMG_0105.JPG', 
							sounds=drum_sounds, parent=self, 
							action=my_button_action, position=scene.Point(sw/6*3, sh/2), 
							animated_icon=True, icon_animation=Animation_Pulse)
		self.buttons.append(self.drum)
		
		self.piano=ButtonNode(size=scene.Size(100, 70), icon='emj:Musical_Keyboard',
							parent=self, action=my_button_action, 
							sounds=piano_sounds, position=scene.Point(sw/6*5, sh/2), 
							animated_icon=True, icon_animation=Animation_Jump)
		self.buttons.append(self.piano)
		
		self.quiter=ButtonNode(size=scene.Size(32, 32), parent=self, 
							action=self.quit, sounds=None,
							position=scene.Point(sw-50, sh-50), text='X', 
							borderColor='black', icon=None)
		self.buttons.append(self.quiter)
		
		
	def quit(self, sender):
		self.view.close()
		
		
	def update(self):
		pass
					
					
	def touch_began(self, touch):
		for btn in self.buttons:
			if self.point_from_scene(touch.location) in btn.frame:
				btn.Button_Tapped()

scene.run(Main())
