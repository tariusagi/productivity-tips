#!/usr/bin/env python3
"""A basic Python 3 TCP echo server using socket module"""
VERSION = "0.1"

# Module imports.
import os
import sys
import getopt
import socket
import signal

# File name and path to this script.
FILE = os.path.basename(__file__)
PATH=os.path.dirname(os.path.abspath(__file__))

# Program usage.
USAGE = f"""\
{FILE} version {VERSION} from {PATH}
Syntax: {FILE} [OPTION] TEXT
A basic Python program that say repeat anything given to it in TEXT.

OPTION:
  -h, --help                  Print this usage.
  -l, --list=host:port        Listen on the given host and port. Default is
                              "127.0.0.1:1234".
  -n, --name=NAME             (Optional) Set the server name. Default "Server".
"""

# Global flag for program termination.
quit = False

def main():
	"""Main function of this program."""
	global quit
	# Default arguments.
	name = "Server"
	host = "127.0.0.1"
	port = 1234
	# Handle commandline arguments.
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hl:n:',
				["help", "listen=", "name="])
	except getopt.error as err:
		print(f'ERROR: {str(err)}. Use "-h" for usage.', file = sys.stderr)
		sys.exit(1)
	for o, v in opts:
		if o in ('-h', '--help'):
			print(USAGE)
			sys.exit(0)
		elif o in ('-l', '--listen'):
			host, port = v.split(':')
			port = int(port)
		elif o in ('-n', '--name'):
			name = v
		else:
			print('ERROR: Unknown option. Use "-h" for usage.', file = sys.stderr);
			sys.exit(2)
	# Set up socket server.
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host, port))
		s.listen()
		print("Server listening on %s:%s." % (host, port))
		while not quit:
			print('Accepting connection...')
			conn, addr = s.accept()
			# A new client.
			print('Connected by', addr)
			conn.sendall(f"{name}: Hi. Say something or \"quit\" to end.\n".encode())
			with conn:
				print('Receiving...')
				while not quit:
					data = conn.recv(1024)
					if data:
						print('Received some data')
						# Decode the received message.
						msg = data.decode('ascii').strip()
						print(f"Received: \"{msg}\" from {addr}.")
						# Handle the extracted command.
						if msg == "quit":
							# Quit command received.
							print("Quitting...")
							conn.sendall(f"{name}: OK, bye!\n".encode())
							quit = True
							break
						else:
							# Echo back or do something else.
							conn.sendall(f"{name}: Received \"{msg}\"\n".encode())
					else:
						print('Nothing received. Client might close the connection.')
						break
				# Close this client's connection.
				print('Closing client connection...')
				conn.shutdown(socket.SHUT_RDWR)
				conn.close()
				print('Client connection closed.')
		# End of service loop. Close the socket.
		print('End of service. Shutting down...')
		s.shutdown(socket.SHUT_RDWR)
		s.close()
		print("Server closed.")

# Entry.
if __name__ == '__main__':
	main()

