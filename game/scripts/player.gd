extends CharacterBody2D

const SPEED = 130.0
const JUMP_VELOCITY = -300.0

# Pega a gravidade do projeto (igual ao RigidBody2D)
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

@onready var animated_sprite = $AnimatedSprite2D

var assist = 0

func _ready():
	add_to_group("player")

func _physics_process(delta):
	# Gravidade
	if not is_on_floor():
		velocity.y += gravity * delta

	# Pulo
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Direção do input: -1, 0, 1
	var direction = Input.get_axis("move_left", "move_right")

	# Flip do sprite
	if direction > 0:
		animated_sprite.flip_h = false
	elif direction < 0:
		animated_sprite.flip_h = true

	# Animações
	if is_on_floor():
		assist = 0
		if direction == 0:
			animated_sprite.play("idle")
		else:
			animated_sprite.play("run")
	else:
		animated_sprite.play("jump")

	# Controle de "perdeu"
	if !is_on_floor():
		assist -= JUMP_VELOCITY
		if assist > 15000:
			position = Vector2(-70.0, 5)
			print("perdeu")

	# Movimento lateral
	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)

	# Movimento final
	move_and_slide()

	# Detecta colisões do frame
	for i in range(get_slide_collision_count()):
		var collision = get_slide_collision(i)
		var collider = collision.get_collider()

		# Pega o Node filho se o grupo estiver lá
		if collider.is_in_group("loser") or collider.get_parent().is_in_group("loser"):
			position = Vector2(-70.0, 5)
			print("perdeu")
		
		if collider.is_in_group("victory") or collider.get_parent().is_in_group("victory"):
			print("ganhou")
			
 
