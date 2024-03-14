## Skill Segregation in Brain without ML

**Learning is a never-ending process for humans.** An average human brain processes a staggering 74 Gigabytes of data each day. Our brains themselves are clusters of separate lobes and nerves, each with its own specialized function. This simple data structures and algorithms project attempts to simulate how this naturally formed distributed system correlates our skills within its storage mechanism, without relying on machine learning models.

**The code implements the following features:**

1. **Simple Web GUI:** Built using Python's Flask framework, allowing user interaction.
2. **User Input:** Captures the name of the skill from the user and displays the current brain model.
3. **Central Node ("Brain")**: Represents the temporal lobe, responsible for storing and retrieving data.
4. **Clustered Graphs:** The code utilizes a clustered graph structure. Each cluster represents a graph containing interrelated elements, similar to how the human brain connects concepts within a specific sense (motor skills, taste, etc.).
5. **Sensory Nodes and Skill Integration:** Each sense has its own cluster of graphs, connected to a sensory node. When a new skill is introduced, if it doesn't correlate with any existing skill graph for a sense node, it becomes the first element of a new cluster within that sense category.

**This project provides a basic model for understanding how the brain might organize and store information related to skills without resorting to machine learning techniques.**
