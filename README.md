# Pacman - Efficient Algorithms Course (EALG)

Old classic Pacman game written in Python using pygame library.

**🎓 Educational Repository**: Used in the Efficient Algorithms (EALG) course. It serves as a foundation for implementing efficient data structures and algorithms. Your work will influence the game difficulty and ghost behavior. After MC1 and MC2, the ghosts will play noticeably better. 🎮

 <img width="892" alt="Screenshot 2024-06-25 at 12 31 20" src="https://github.com/MathMark/PacMan/assets/13971845/19fa8ce2-a5ed-4cb2-81d6-0130cdf5268e">


# 🛠️ Implementation Guide

You are expected to complete the provided empty methods in [priority_queue](model/algorithms/priority_queue.py) and [pathfinding](model/algorithms/pathfinding.py). 

Do not remove or modify the existing method signatures. If necessary, you may add additional helper methods.

## What to Change Where in the Code

- **Priority Queue** (MC1): Implement your efficient version in `priority_queue.py`. Replace the placeholder with your own solution.
- **Pathfinding Algorithm** (MC2): Implement your algorithm in `pathfinding.py`. Add an A* based solution or machine learning (ML) based ghost movement strategy.
- **Ghost AI** (MC2): Modify `ghosts.py`. Integrate your pathfinding into the `Ghost.calc_distance(...)` method.
- **Settings** (`settings.py`): Adjust the parameter `USE_PATHFINDING = True | False` to evaluate your algorithm under different conditions.

## Notes

- The game will not change after you complete MC1.
- The effects will only become visible once you implement the components required for MC2.
- “The show must go on.” 🔛 The game must remain playable at every stage.
- You are expected to implement all methods with missing bodies, except those marked as “Optional to implement.”
- Please review the evaluation criteria carefully, ideally before starting to code and, before submission.

# 📋 Student Submission Guide

## Milestone Branches

Students must submit their work on two milestone branches:

- **`mc1`** - Milestone 1: Implement an efficient data structure from scratch, specifically a priority queue.
- **`mc2`** - Milestone 2: Implement an efficient pathfinding algorithm, with or without ML.

## How to Submit Your Work

1. **Create your MC branch** from the main branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b mc<1|2>_<your surname_name>
   ```

2. **Make your changes** and test locally:
   ```bash
   python pacman.py
   ```

3. **Commit with clear messages**:
   ```bash
   git commit -m "Describe what you did"
   ```

4. **Push to your feature branch**:
   ```bash
   git push origin <your_branch>
   ```

5. **Create a Pull Request** targeting the appropriate milestone branch (`mc1` or `mc2`):
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Set base branch to `mc1` or `mc2` (depending on milestone)
   - Select your feature branch
   - Add a description of your implementation

6. **Wait for review** - Your code will be reviewed and graded five days after the specified deadline in the course calendar. During these five days, you may still make changes and resubmit your work. However, each additional day on which you submit changes will reduce your grade by five percent.

## Requirements for Grading

- ✅ A clear commit history that reflects your development process, with meaningful commit messages
- ✅ Clean and readable code that follows consistent style and structure
- ✅ Well commented code that explains your algorithmic choices and design decisions
- ✅ An efficient implementation, algorithmic complexity matters and should be justified where relevant
- ✅ Proper testing of your implementation before submission
- ✅ The code must run without crashing at every stage. Even after MC1, when the game behavior does not change, the project must remain fully runnable
- ✅ No plagiarism, submit your own original solutions


# Description (from the original repo)

The game contains a single demo-level. To increase difficulty you can play around with variables in settings file changing POWERUP_LIMIT, SCATTER_DISABLE_TRIGGER, SCATTER_ENABLE_TRIGGER, VELOCITY. You can also set 
variable DEBUG to True to see ghosts targets visualization and grid.

## Ghosts behaviour

| Name   | Description  | Behaviour                                                                                                                                                                                                                                                               |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Blinky | Red Ghost    | Follows Pac-Man directly during Chase mode, and heads to the upper-right corner during Scatter mode.                                                                                                                                                                    |
| Pinky  | Pink ghost   | Chases towards the spot 2 Pac-Dots in front of Pac-Man. Due to a bug in the original game's coding, if Pac-Man faces upwards, Pinky's target will be 2 Pac-Dots in front of and 2 to the left of Pac-Man. During Scatter mode, she heads towards the upper-left corner. |
| Inky   | Blue ghost   | During Chase mode, his target is a bit complex. His target is relative to both Blinky and Pac-Man, where the distance Blinky is from Pinky's target is doubled to get Inky's target. He heads to the lower-right corner during Scatter mode.                            |
| Clyde  | Yellow ghost | Chases directly after Pac-Man, but tries to head to his Scatter corner when within an 8-Dot radius of Pac-Man. His Scatter Mode corner is the lower-left.                                                                                                               |

