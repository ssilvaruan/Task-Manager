# TaskCLI

A simple task manager written in Python and run straight from the terminal. It lets you add, list, complete, and remove tasks, storing the data locally in a JSON file.

## Features

- **Add tasks:** Create new tasks with custom titles.
- **List tasks:** View all tasks or only the pending ones.
- **Complete tasks:** Mark tasks as done using their IDs.
- **Remove tasks:** Delete tasks you no longer need.
- **Local storage:** Data is saved automatically to a `tarefas.json` file in the same folder as the script.
- **Safe writes:** The file is saved atomically, preventing data loss if something fails mid-write.
- **Clear error messages:** Empty titles, unknown IDs, and invalid JSON files are handled with simple warnings.

## Technologies

- Python 3 (no external dependencies)
- JSON
- Argparse
- Pathlib, OS, and Tempfile

## Getting started

**1. Clone the repository**

```bash
git clone https://github.com/ssilvaruan/TaskCLI.git
```

**2. Enter the project folder**

```bash
cd TaskCLI
```

**3. Run the commands**

Add a task:

```bash
python taskmanager.py add "Study Python"
```

List all tasks:

```bash
python taskmanager.py list
```

List only pending tasks:

```bash
python taskmanager.py list --pendentes
```

Complete a task:

```bash
python taskmanager.py done 1
```

Remove a task:

```bash
python taskmanager.py remove 1
```

Show help for all commands:

```bash
python taskmanager.py --help
```

## Usage example

```text
$ python taskmanager.py add "Study Python"
Tarefa #1 adicionada.

$ python taskmanager.py add "Review code"
Tarefa #2 adicionada.

$ python taskmanager.py done 1
Tarefa #1 concluída.

$ python taskmanager.py list
  1 [x] Study Python
  2 [ ] Review code
```

> **Note:** the program's messages are in Portuguese.

## Data format

Tasks are stored in `tarefas.json` as a list of objects:

```json
[
  {
    "id": 1,
    "titulo": "Study Python",
    "feita": true
  }
]
```

Field names: `id` (task number), `titulo` (title), `feita` (done).

## Project structure

```text
TaskCLI/
│
├── taskmanager.py
├── tarefas.json
└── README.md
```

The `tarefas.json` file is created automatically when the first task is added.

## Purpose

This project was built to practice core Python concepts such as file handling, data structures, functions, command-line arguments, and data persistence using JSON.

---

**Developed by [Ruan S. Silva](https://github.com/ssilvaruan)**