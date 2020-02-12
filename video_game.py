import turtle
import game_settings


wn = turtle.Screen()
wn.title("AoI Concept")
turtle.fd(0)
turtle.speed(0)
wn.bgcolor("white")
turtle.ht()
turtle.setundobuffer(None)
turtle.delay(1)
# turtle.tracer(20,0)
turtle.register_shape("tank.gif")
turtle.register_shape("drone1.gif")
turtle.register_shape("drone2.gif")
turtle.register_shape("antenna.gif")
turtle.register_shape("bullet.gif")


class Bullet(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.hideturtle()
		self.shape("arrow")
		self.penup()
		self.speed(8)
		self.color("black")
		self.fd(0)
		self.goto(0, 0)
		self.shape("bullet.gif")

class Player(turtle.Turtle):
	def __init__(self, spriteshape, color, startx, starty):
		turtle.Turtle.__init__(self, shape = "antenna.gif")
		self.hideturtle()
		self.speed(3)
		self.penup()
		self.color(color)
		self.fd(0)
		self.goto(startx, starty) # for the actual values, see game_settings.py and the declaration of the player object
		self.left(90)
		self.showturtle()
	
# player's controls defined

	def move(self):
		self.fd(5)
	def turn_left(self):
		self.lt(5)
	def turn_right(self):
		self.rt(5)
	def accelerate(self):
		self.move()

# Define Enemy1 class, will move in a circle
class Enemy1(turtle.Turtle):

	def __init__(self, spriteshape, color, startx, starty): 
		turtle.Turtle.__init__(self, shape = "drone1.gif")
		self.hideturtle
		self.speed(3)
		self.penup()
		self.color(color)
		self.fd(0)
		self.setposition(startx, starty)
		self.bullet_list1 = []
		self.freq1 = game_settings.freq1 # frequency of shooting


	def move1(self):  # circle movement drone
		self.rt(2)
		self.fd(2)
		self.freq1 = self.freq1 - 1 # reduce count for every step, fire when step equals frequency. then reset the count
		if (self.freq1==30.):
			#(x_z, y_z) = self.pos()
			#self.goto(x_z,y_z+100)
			self.dot(5,'blue')
		if (self.freq1==0):
			#self.goto(x_z, y_z)
			self.clear()
			self.enemy1_fire()
			self.freq1 = game_settings.freq1

	def move_bullet1(self,bullet_list1):
		for bullet in self.bullet_list1:
			y = bullet.ycor()
			y1 = y - game_settings.bullet_speed
			bullet.sety(y1)

		for bullet in self.bullet_list1:
			if (bullet.ycor()>game_settings.y_max or bullet.xcor()>game_settings.x_max or bullet.ycor()<game_settings.x_min or bullet.xcor()<game_settings.y_min):
				bullet.hideturtle()
				bullet.clear()
				self.bullet_list1.remove(bullet)
				# print(len(enemy1.bullet_list))


	def enemy1_fire(self):
		x = self.xcor()
		y = self.ycor()
		bullet1 = Bullet()
		bullet1.setposition(x,y) # bullet will appear just above the player
		bullet1.setheading(270) # make it face downwards
		bullet1.showturtle()
		self.bullet_list1.append(bullet1)

num_Enemy1 = 1
enemies1 = []
for i in range(num_Enemy1):
	b = Enemy1("circle", "red", game_settings.x1, game_settings.y1)
	enemies1.append(b)

# Enemy1 class defined 

# define Enemy2 class, will move in a square. drone
class Enemy2(turtle.Turtle):

	def __init__(self, spriteshape, color, startx, starty):
		turtle.Turtle.__init__(self, shape = "drone2.gif")
		self.hideturtle
		self.speed(1)
		self.penup()
		self.color(color)
		self.fd(0)
		self.setheading(0)
		self.setposition(startx, starty)
		self.bullet_list2 = []
		self.freq2 = game_settings.freq2 # frequency of shooting
		self.square_size = 200
		self.startx = startx
		self.starty = starty
		self.speed2 = game_settings.speed2 # pixels to move per time slot
		#print("Starting positions are:", startx, ", ", starty)


	def move2(self): # square
		#print (self.heading())
		if self.heading() == 0: # when moving right, condition for left turn is exceeding the square dimension
			#print {"left 1"}
			if (abs(self.xcor()-self.startx))>self.square_size:
				self.lt(90)

		if self.heading() == 90: # when going up, condition for left turn is exceeding the square dimension
			#print {"left 2"}
			if (abs(self.ycor()-self.starty))>self.square_size:
				self.lt(90)
		
		if self.heading() == 180: # when going left, condition for left turn is the x-coordinates of the starting point and it's current position being same
			#print {"left 3"}
			if int(abs(self.xcor()-self.startx))==0:
				self.lt(90)
		
		if self.heading() == 270: # when going down, condition for left turn is the y-coordinates of the starting point and it's current position being same
			#print {"left 4"}
			if int(abs(self.ycor()-self.starty))==0:
				self.lt(90)

		self.fd(self.speed2)

		self.freq2 = self.freq2 - 1
		if (self.freq2==50.):
			#(x_z, y_z) = self.pos()
			#self.goto(x_z,y_z+100)
			self.dot(8,'red')
		if (self.freq2==0):
			self.clear()
			self.enemy2_fire()
			self.freq2 = game_settings.freq2

	def move_bullet2(self,bullet_list2):
		for bullet in self.bullet_list2:
			y = bullet.ycor()
			y1 = y - game_settings.bullet_speed
			bullet.sety(y1)

		for bullet in self.bullet_list2:
			if (bullet.ycor()>game_settings.y_max or bullet.xcor()>game_settings.x_max or bullet.ycor()<game_settings.x_min or bullet.xcor()<game_settings.y_min):
				bullet.hideturtle()
				bullet.clear()
				self.bullet_list2.remove(bullet)
				# print(len(enemy1.bullet_list))


	def enemy2_fire(self):
		x = self.xcor()
		y = self.ycor()
		#print("vehicle 2's location are:",x, ", ",y)
		bullet2 = Bullet()
		bullet2.setposition(x,y) # bullet will appear just above the player
		bullet2.setheading(270)
		bullet2.showturtle()
		self.bullet_list2.append(bullet2)

num_Enemy2 = 1
enemies2 = []
for i in range(num_Enemy2):
	b = Enemy2("circle", "red", game_settings.x2 , game_settings.y2)
	enemies2.append(b)

# Enemy3 class defined

class Enemy3(turtle.Turtle):

	def __init__(self, spriteshape, color, startx, starty): # green
		turtle.Turtle.__init__(self, shape = "tank.gif")
		self.hideturtle
		self.speed(1)
		self.penup()
		self.color(color)
		self.fd(0)
		self.setposition(game_settings.x3, game_settings.y3)
		self.bullet_list3 = []
		self.freq3 = game_settings.freq3
		self.speed3 = game_settings.speed3
	

	def enemy3_fire(self):
		x = self.xcor()
		y = self.ycor()
		bullet3 = Bullet()
		bullet3.setposition(x,y-40) # bullet will appear just below the player
		bullet3.setheading(270)
		bullet3.showturtle()
		self.bullet_list3.append(bullet3)

	def move3(self): # left and right sweeping across the x axis
		self.freq3 = self.freq3 - 1
		if (self.freq3==40):
			#(x_z, y_z) = self.pos()
			#self.goto(x_z,y_z+100)
			self.dot(10,'brown')
		if (self.freq3==0):
			self.clear()
			self.enemy3_fire()
			self.freq3 = game_settings.freq3
		x = self.xcor()
		x = x + self.speed3
		self.setx(x)
		if self.xcor() > (game_settings.x_max-200) or self.xcor() < (game_settings.x_min+200): # sweeping just the central part of the area
			self.speed3  = self.speed3 * (-1) # change speed direction to left when at boundary

	def move_bullet3(self,bullet_list3):
		for bullet in self.bullet_list3:
			y = bullet.ycor()
			y1 = y - game_settings.bullet_speed
			bullet.sety(y1)

		for bullet in self.bullet_list3:
			if (bullet.ycor()>game_settings.y_max or bullet.xcor()>game_settings.x_max or bullet.ycor()<game_settings.x_min or bullet.xcor()<game_settings.y_min):
				bullet.hideturtle()
				bullet.clear()
				self.bullet_list3.remove(bullet)
				# print(len(enemy1.bullet_list))





num_Enemy3 = 1
enemies3 = []
for i in range(num_Enemy3):
	b = Enemy3("circle", "red", game_settings.x3, game_settings.y3)
	enemies3.append(b)

# Enemy3 class defined

player = Player("triangle", "white", game_settings.x_player, game_settings.y_player)

#key bindings
turtle.listen()
turtle.onkey(player.turn_left,"Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate,"Up")
#turtle.onkey(player.brake,"Down")

while True:

	# enemy 1 loop

	for enemy1 in enemies1:
		enemy1.move1()
		enemy1.move_bullet1(enemy1.bullet_list1)
		
	# enemy 2 loop

	for enemy2 in enemies2:
		enemy2.move2()
		enemy2.move_bullet2(enemy2.bullet_list2)

	# enemy 3 loop

	for enemy3 in enemies3:
		enemy3.move3()
		enemy3.move_bullet3(enemy3.bullet_list3)

delay = raw_input("Press enter to finish. > ")
