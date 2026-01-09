extends Node

const UDP_PORT_P1 = 9000
const UDP_PORT_P2 = 9001

var server_p1 = PacketPeerUDP.new()
var server_p2 = PacketPeerUDP.new()

@onready var p1_node = $player_01
@onready var p2_node = $player_02 

func _ready():
	# 1. Start Servers
	if server_p1.bind(UDP_PORT_P1) == OK:
		print("P1 Listening on ", UDP_PORT_P1)
	if server_p2.bind(UDP_PORT_P2) == OK:
		print("P2 Listening on ", UDP_PORT_P2)
		
	# 2. Link Players (So they can hit each other)
	if p1_node and p2_node:
		p1_node.opponent = p2_node
		p2_node.opponent = p1_node
		print("Players linked as opponents.")

func _process(_delta):
	# P1 Listener
	while server_p1.get_available_packet_count() > 0:
		var pkt = server_p1.get_packet()
		if is_instance_valid(p1_node):
			p1_node.receive_command(pkt.get_string_from_utf8())

	# P2 Listener
	while server_p2.get_available_packet_count() > 0:
		var pkt = server_p2.get_packet()
		if is_instance_valid(p2_node):
			p2_node.receive_command(pkt.get_string_from_utf8())

func _exit_tree():
	server_p1.close()
	server_p2.close()
