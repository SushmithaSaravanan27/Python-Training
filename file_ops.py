def read_file(name):
    with open(name, 'r') as f:
        return f.read()
def write_file(name, text):
    with open(name, 'w') as f:
        f.write(text)
