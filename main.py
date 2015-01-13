import rapiro as r
import curses

x = r.Rapiro()
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Using Up, Left and Right arrow to control the rover. Hit 'q' to quit")
stdscr.refresh()

key = ''
try:
	while key != 27:
		key = stdscr.getch()
		stdscr.addch(20,25,key)
		stdscr.refresh()
		if key == curses.KEY_UP:
			x.forward()
		elif key == curses.KEY_DOWN:
			x.backward()
		elif key == curses.KEY_LEFT:
			x.turn_left()
		elif key == curses.KEY_RIGHT:
			x.turn_right()
		elif key in map(lambda i:ord(str(i)),[1,2,3,4,5,6,7,8,9,0]):
			x.action(int(chr(key)))
		elif key == ord('h'):
			x.head_left()
		elif key == ord('H'):
			x.head_right()
		elif key == ord('w'):
			x.waist_left()
		elif key == ord('W'):
			x.waist_right()
		elif key == ord('q'):
			x.left_shoulder_y_left()
		elif key == ord('Q'):
			x.left_shoulder_y_right()
		elif key == ord('p'):
			x.right_shoulder_y_left()
		elif key == ord('P'):
			x.right_shoulder_y_right()
		elif key == ord('a'):
			x.left_shoulder_p_left()
		elif key == ord('A'):
			x.left_shoulder_p_right()
		elif key == ord('l'):
			x.right_shoulder_p_left()
		elif key == ord('L'):
			x.right_shoulder_p_right()
		elif key == ord('z'):
			x.left_hand_left()
		elif key == ord('Z'):
			x.left_hand_right()
		elif key == ord(','):
			x.right_hand_left()
		elif key == ord('<'):
			x.right_hand_right()
		elif key == ord('s'):
			x.left_foot_y_left()
		elif key == ord('S'):
			x.left_foot_y_right()
		elif key == ord('k'):
			x.right_foot_y_left()
		elif key == ord('K'):
			x.right_foot_y_right()
		elif key == ord('x'):
			x.left_foot_p_left()
		elif key == ord('X'):
			x.left_foot_p_right()
		elif key == ord('m'):
			x.right_foot_p_left()
		elif key == ord('M'):
			x.right_foot_p_right()
		elif key == ord('i'):
			x.reset()
		elif key == ord('f'):
			x.look_for_face()
except Error as e:
	raise(e)
finally:	
	curses.endwin()
