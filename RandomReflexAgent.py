from agents import *
from notebook import psource
import random

class ContinuousXYEnvironment(XYEnvironment):
    """This class is for environments on a 2D plane, with continuous locations.
    Agents perceive things within a radius. Each agent in the environment has a
    .location slot which should be a location such as (x, y), and a .holding slot,
    which should be a list of things that are held."""

    def __init__(self, width=10, height=10):
        super().__init__(width, height)

    def is_inbounds(self, location):
        """Checks to make sure that the location is inbounds."""
        x, y = location
        return not (x < self.x_start or x > self.x_end or y < self.y_start or y > self.y_end)

    def random_location_inbounds(self, exclude=None):
        """Returns a random location that is inbounds."""
        location = (round(random.uniform(self.x_start, self.x_end)),
                    round(random.uniform(self.y_start, self.y_end)))
        if exclude is not None:
            while location == exclude:
                location = (round(random.uniform(self.x_start, self.x_end)),
                            round(random.uniform(self.y_start, self.y_end)))
        return location
    
    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'right':
            agent.direction = Direction(Direction.R)
            agent.performance -= 1
            self.move_to(agent, agent.direction.move_forward(agent.location))
        elif action == 'left':
            agent.direction = Direction(Direction.L)
            agent.performance -= 1
            self.move_to(agent, agent.direction.move_forward(agent.location))
        elif action == 'up':
            agent.direction = Direction(Direction.U)
            agent.performance -= 1
            self.move_to(agent, agent.direction.move_forward(agent.location))
        elif action == 'down':
            agent.direction = Direction(Direction.D)
            agent.performance -= 1
            self.move_to(agent, agent.direction.move_forward(agent.location))
        elif action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list != []:
                dirt = dirt_list[0]
                agent.performance += 100
                self.delete_thing(dirt)



class VacuumEnvironment(ContinuousXYEnvironment):
    """The environment for the modified vacuum agent."""
    def __init__(self, width=10, height=10, dirt_density=0.8):
        super().__init__(width, height)
        self.add_walls()
        self.add_dirt(dirt_density)

    def thing_classes(self):
        return [Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """The percept is a tuple of ('Dirty' or 'Clean', 'Bump' or 'None')."""
        x, y = agent.location
        rounded_location = (round(x), round(y))  # Round the location to the nearest integer
        status = ('Dirty' if self.some_things_at(rounded_location, Dirt) else 'Clean')
        bump = ('Bump' if agent.bump else 'None')
        return status, bump

    def add_dirt(self, dirt_density):
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < dirt_density:
                    self.add_thing(Dirt(), (x,y))
                # Uncomment to add random walls in the environment
                # else:
                #     self.add_thing(Wall(), (x,y))
    
    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do. If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()
        
def SimpleReflexAgentProgram():
    """This agent takes action based solely on the percept."""
    def program(percept):
        status, bump = percept
        if status == 'Dirty':
            print("Agent chose to suck")
            return 'Suck'
        else:
            action = random.choice(['right', 'left', 'up', 'down'])
            print("Agent chose to move", action)
            return action

    return program

if __name__ == "__main__":
    psource(ContinuousXYEnvironment)

    # Keep count of the number of times a room in the environment is dirty or clean
    dirty_count = 0 
    clean_count = 0 
    
    # Initialize the continuous environment
    vac_env = VacuumEnvironment()
    program = SimpleReflexAgentProgram()
    simple_reflex_agent = Agent(program)

    # Checks the initial state of the environment
    vac_env.add_thing(simple_reflex_agent)

    for i in range(100):
        print("Iteration:", i+1)
        
        # Check if the current location is dirty or clean
        status, _ = vac_env.percept(simple_reflex_agent)
        if status == "Dirty":
            dirty_count += 1
        elif status == "Clean":
            clean_count += 1        
        
        # Randomly move the agent
        vac_env.step()

    print("Amount of times a location was identified as dirty:", dirty_count)
    print("Amount of times a location was identified as clean:", clean_count)
    print("Agent's performance score:", simple_reflex_agent.performance)