extends CharacterBody2D

# --- SETTINGS ---
const SPEED = 300.0
const JUMP_FORCE = -500.0
const GRAVITY = 980.0
const ATTACK_RANGE = 80.0 # Pixels
const DAMAGE_LIGHT = 10
const DAMAGE_HEAVY = 20

# --- NODES ---
@onready var anim = $AnimatedSprite2D
# Assigned by Main.gd
var opponent: CharacterBody2D = null

# --- STATE ---
var health = 100
var is_dead = false
var is_attacking = false
var current_command = "idle"
var attack_gesture_held = false
var time_since_last_command = 0.0

func _ready():
	anim.animation_finished.connect(_on_animation_finished)

# --- COMMAND HANDLING ---
func receive_command(cmd: String):
	if is_dead: return
	current_command = cmd
	time_since_last_command = 0.0

# --- DAMAGE SYSTEM ---
func take_damage(amount):
	if is_dead: return
	
	health -= amount
	print(name, " Health: ", health)
	
	if health <= 0:
		die()
	else:
		# Optional: Interrupt attack to play hit animation
		is_attacking = true # Lock movement briefly
		play_anim("take_hit")

func die():
	is_dead = true
	is_attacking = false
	current_command = "idle"
	play_anim("death")
	# Disable collision if you want:
	# $CollisionShape2D.set_deferred("disabled", true)

# --- PHYSICS LOOP ---
func _physics_process(delta):
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	if is_dead:
		move_and_slide()
		return

	# Watchdog
	time_since_last_command += delta
	if time_since_last_command > 0.2:
		current_command = "idle"

	# Logic
	if not is_attacking:
		handle_movement()
		handle_attacks()
	else:
		# Stop sliding while attacking/hurt
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()

func handle_movement():
	if current_command == "move_right":
		velocity.x = SPEED
		anim.flip_h = false
		if is_on_floor(): play_anim("run")
		attack_gesture_held = false # Release lock
		
	elif current_command == "move_left":
		velocity.x = -SPEED
		anim.flip_h = true
		if is_on_floor(): play_anim("run")
		attack_gesture_held = false # Release lock
		
	elif current_command == "jump" and is_on_floor():
		velocity.y = JUMP_FORCE
		play_anim("jump")
		current_command = "idle"
		
	elif current_command == "idle":
		velocity.x = move_toward(velocity.x, 0, SPEED)
		if is_on_floor(): play_anim("idle")
		attack_gesture_held = false # Release lock

func handle_attacks():
	if "attack" in current_command:
		if not attack_gesture_held:
			attack_gesture_held = true
			
			if current_command == "attack_1":
				perform_attack("attack_1", DAMAGE_LIGHT)
			elif current_command == "attack_2":
				perform_attack("attack_2", DAMAGE_HEAVY)

func perform_attack(anim_name, damage):
	is_attacking = true
	play_anim(anim_name)
	
	# HIT DETECTION
	if opponent and is_instance_valid(opponent) and not opponent.is_dead:
		var dist = global_position.distance_to(opponent.global_position)
		
		# Check 1: Range
		if dist < ATTACK_RANGE:
			# Check 2: Facing Direction
			# If I'm facing right (flip_h=false), enemy x must be > my x
			var facing_enemy = false
			if anim.flip_h == false and opponent.global_position.x > global_position.x:
				facing_enemy = true
			elif anim.flip_h == true and opponent.global_position.x < global_position.x:
				facing_enemy = true
			
			if facing_enemy:
				opponent.take_damage(damage)

func play_anim(name):
	if anim.animation != name:
		anim.play(name)

func _on_animation_finished():
	# If we finished an attack or hit reaction, return to control
	if anim.animation in ["attack_1", "attack_2", "take_hit"]:
		is_attacking = false
		play_anim("idle")
	# Death animation just stays at the last frame (ensure Loop is OFF)
