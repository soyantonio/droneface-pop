# Droneface pop
Point of present of a droneface internal server

## Table of contents
* [Table of contents](#table-of-contents)
* [Entrypoints](#entrypoints)
* [Extra commands](#extra-commands)

## Entrypoints

This project was developed and can be implemented in different forms. The `LoadTrained.py` is the simplest one. It will open a window with a face recognition app

```bash
python LoadTrained.py
```

Another approach is via a local streaming server using flask and opencv. This will open an app at http://localhost:5001 

```bash
python app.py
```

The third approach is **still in progress**, it is intended to work as a redirection entrypoint

```bash
python pop.py
```

## Extra commands
```bash
pip install opencv-contrib-python
```

Run

```bash
python app.py
```

Or

```bash
python -m flask run
```