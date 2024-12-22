# 🎄 Advent of Code Solutions in Python

![Advent of Code](https://img.shields.io/badge/Advent%20of%20Code-Yearly-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)

This repository contains my solutions to the Advent of Code challenges for various years, implemented in Python. Advent of Code is an annual coding event with daily programming puzzles throughout the month of December. These solutions are my personal implementations and are meant for educational purposes.

## 📋 Table of Contents

- [Overview](#overview)
- [How to Use](#how-to-use)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

Advent of Code is a fantastic way to improve your programming skills, problem-solving abilities, and familiarity with different algorithms and data structures. This repository serves as a record of my solutions to the challenges posed in Advent of Code for multiple years. Feel free to explore the solutions, learn from them, and provide feedback if you have suggestions for improvement.

## 🚀 How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/MoeFourtyTwo/advent-of-code.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd advent-of-code
   ```

3. **Install Dependencies with uv:**
   ```bash
   uv sync
   ```

4. **Set Up Your Session Token:**
   Create a `.env` file in the project root with the following content:
   ```env
   AOC_SESSION=your_session_token
   ```
   Replace `your_session_token` with your Advent of Code session token, which you can obtain from [Advent of Code](https://adventofcode.com/).

5. **Run the Python Script:**
   ```bash
   uv run exec run --year <year> --day <day> --part <part>
   ```

   Replace `<year>`, `<day>`, and `<part>` with the corresponding values. Any omitted value will be extracted from the current date.

6. **Use Templates to Generate Starting Points For New Solutions:**

   ```bash
   uv run exec generate --year <year> --day <day> --part <part>
   ```
   
   Replace `<year>`, `<day>`, and `<part>` with the corresponding values. Any omitted value will be extracted from the current date.

## 📁 Directory Structure

- **aoc/**
  - **common/**
    - Utility functions shared across multiple solutions.

- **aoc/tasks/**
  - **year_<year>/**
    - **day_<day>/**
      - `part_1.py`: Python script containing the solution for part 1.
      - `part_2.py`: Python script containing the solution for part 2.
      - 
- **aoc/tasks/**
  - **_template_day/**
    - Contains the template for the solutions.

- **aoc/runner.py**
  - Runner CLI that generates empty solutions and is the entry point to run solutions.

- **data/**
  - **year_<year>/**
    - **day_<day>/**
      - `example.txt`: Example input data for testing.

- **tests/**
  - **tasks/**
    - **year_<year>/**
      - **day_<day>/**
        - `test_part_1.py`: Python script with tests for part 1.
        - `test_part_2.py`: Python script with tests for part 2.

- ...

## 🤝 Contributing

If you have alternative solutions, improvements, or suggestions, feel free to open an issue or submit a pull request. I welcome collaboration and diverse perspectives!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Happy coding! 🚀