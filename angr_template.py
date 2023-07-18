import claripy
import angr
import sys
import logging


def is_successful(state):
    # successful print
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Flag Captured!' in stdout_output


def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    # needs abort
    if any(x in [b'You lost! You consumed all your candy and starved', b'You hit a wall! Tough luck'] for x in
           stdout_output):
        return True  
    else:
        return False


# logging.getLogger('angr').setLevel(logging.INFO)

finds = 0x00400afd  # if you know the address where to the end goal is
avoid = 0x00400c58  # if you know what address to avoid

path = "./metaverse"
project = angr.Project(path)

# flag_chars = [claripy.BVS("flag_%d" % i, 8) for i in range(32)]
# flag = claripy.Concat(*flag_chars)

flag = claripy.BVS("flag", 8 * 32)

# state = project.factory.entry_state(stdin = flag)

state = project.factory.entry_state(stdin=flag, add_options={angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
                                                             angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS})  # if you don't know where to start

# address_of_target = project.loader.find_symbol("print_flag").rebased_addr # find address of specific methods

# f = project.factory.callable(addr=address_of_target)

# state = project.factory.blank_state(addr=0x00400be4, stdin=flag, add_options={
# angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY, angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS})  # if you need to start at somewhere

# state.regs.eax = flag_chars[0]
# state.regs.ebx = flag_chars[1]
# state.regs.edx = flag_chars[2]

# CTF prefix:
# state.solver.add(flag.get_byte(0) == ord('e'))

from string import printable

for i in range(32):  # setting a constraint that the letters will be ascii
    state.solver.add(
        claripy.Or(*(
            flag.get_byte(i) == x
            for x in printable
        ))
    )

simulation = project.factory.simgr(state) # veritesting=True

print(simulation.active[0]) # find offset. 

simulation.explore(find=is_successful, avoid=should_abort)

if simulation.found:
    solution = simulation.found[0]
    print(solution.posix.dumps(sys.stdin.fileno()))
    # print(solution.solver.eval(flag))
else:
    print("no solution")

# print(f(0x824,0x82c,0x82b))

# print(f.result_state.posix.stdout.concretize())


