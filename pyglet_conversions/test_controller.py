from controllerIO import Controller
import keyboardInput as KB
num = 0
CONTROLLER_NUMBER1 = 0
CONTROLLER_NUMBER2 = 1

test_controller1 = Controller(CONTROLLER_NUMBER1)
test_controller2 = Controller(CONTROLLER_NUMBER2)

running = True

while running:
    inp1 = test_controller1.getInput()
    inp2 = test_controller2.getInput()
    if inp1 or inp2:
        print(inp1, inp2, num)
        num += 1
    if KB.SELECT in inp1:
        running = False


print("Ended Test")
    

