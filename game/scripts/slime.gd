extends Node2D

const SPEED = 50

# limites de movimento no eixo X
@export var min_x: float = 300
@export var max_x: float = 380

var moving_right = true

@onready var animated_sprite = $AnimatedSprite2D

func _process(delta):
	animated_sprite.play("idle")

	if moving_right:
		position.x += SPEED * delta
		animated_sprite.flip_h = false
		if position.x >= max_x:
			moving_right = false
	else:
		position.x -= SPEED * delta
		animated_sprite.flip_h = true
		if position.x <= min_x:
			moving_right = true
