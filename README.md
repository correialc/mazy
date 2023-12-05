## Mazy

![CICD](https://github.com/correialc/mazy/actions/workflows/mazy-cicd.yml/badge.svg)
![python-versions](https://img.shields.io/badge/python-3.11+-blue.svg)
![GitHub License](https://img.shields.io/github/license/correialc/mazy)

This is an exploratory project to create maze builders and solvers in Python. 

Working with maze algorithms is fun and creates different opportunities to explore problems in Computer Science. 

The project is aimed at students and enthusiasts of maze algorithms. It's also a fun place for Python programmers.


### Getting Started

- Clone the project repository from Github
- From the project's root folder, run `pip install mazy`
- Run `python maze_maker.py`

Additional help is provided using GNU standard -h or --help.


### Architecture

---

```mermaid
flowchart LR
    CLI[Mazy CLI]
    BTG[Binary Tree]
    SW[Sidewinder]
        
    ASC[ASCII]
    DESK[Desktop GUI]

    subgraph MVP[v0.2.0]
        subgraph Builders
            BTG
            SW 
        end

        subgraph Viewers
            ASC
            DESK
        end

        CLI-->Builders
        CLI-->Viewers
    end
```

### Coming next...

```mermaid
flowchart LR
    CLI[Mazy CLI]
    BTG[Binary Tree]
    SW[Sidewinder]
    DIJK[Shortest Path]

    ASC[ASCII]
    DESK[Desktop GUI]
    SVG[SVG File]

    subgraph MVP[v0.3.0]
        subgraph Builders
            BTG
            SW 
        end

        subgraph Viewers
            ASC
            DESK
        end

        subgraph Solvers
            DIJK
        end

        subgraph Exporters
            SVG
        end

        CLI-->Builders
        CLI-->Viewers
        CLI-->Solvers
        CLI-->Exporters
    end
```