#!/usr/bin/python3.10
def init():
    import os
    if not os.path.exists('/opt/dailytasks/tasks'):
        os.system('mkdir /opt/dailytasks/ -p')
        os.system('touch /opt/dailytasks/tasks')
        return

def main():
    init()
    lines = (line.rstrip('\n') for line in open('/opt/dailytasks/tasks'))
    c = 1
    for line in lines:
        input(f"{c}. {line}: ")
        c += 1

if __name__ == "__main__":
    main()
