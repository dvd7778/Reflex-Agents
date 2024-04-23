from agents import *
from notebook import psource
import random


def SimpleReflexAgentProgram():
    """This agent takes action based solely on the percept. [Figure 2.10]"""

    def program(percept):
        room, status = percept
        return 'Suck' if status == 'Dirty' else 'Right' if room == loc_A else 'Left'

    return program

if __name__ == "__main__":
    psource(TrivialVacuumEnvironment)

    # Keep count of the number of times a room in the environment is dirty or clean
    dirty_count = 0 
    clean_count = 0 

    # Initialize the two-state environment
    triv_vac_env = TrivialVacuumEnvironment()
    program = SimpleReflexAgentProgram()
    simple_reflex_agent = Agent(program)

    # Checks the initial state of the environment
    triv_vac_env.add_thing(simple_reflex_agent)
    print("State of the Environment: {}.".format(triv_vac_env.status))
    print("SimpleReflexVacuumAgent is located at {}.\n".format(simple_reflex_agent.location))

    for i in range(10):
        print("Iteration:", i+1)
        room_to_dirty = random.randint(0, 2) # Chooses a random number from 0 to 2
        if room_to_dirty in [0, 1]: # 0 and 1 mean the left or right room became dirty 
            print("Room {} was made dirty".format(room_to_dirty))
            triv_vac_env.status[room_to_dirty, 0] = "Dirty"
        # 2 means none of the rooms became dirty
        
        # Print current state of the environment
        print("State of the Environment: {}.".format(triv_vac_env.status))
        print("SimpleReflexVacuumAgent is located at {}.".format(simple_reflex_agent.location))
        
        # Runs the environment by one step
        triv_vac_env.step()

        # Verifies the new current state of the environment
        print("State of the Environment: {}.".format(triv_vac_env.status))
        print("SimpleReflexVacuumAgent is located at {}.\n".format(simple_reflex_agent.location))
        if triv_vac_env.status[1,0] == "Dirty":
            dirty_count += 1
        if triv_vac_env.status[0,0] == "Dirty":
            dirty_count += 1
        if triv_vac_env.status[1,0] == "Clean":
            clean_count += 1
        if triv_vac_env.status[0,0] == "Clean":
            clean_count += 1

    print("Amount of times a room was identified as dirty:", dirty_count)
    print("Amount of times a room was identified as clean:", clean_count)
    print("Agent's performance score:", simple_reflex_agent.performance)