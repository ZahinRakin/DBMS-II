def atomicRecovery(log):
    undo = set()
    redo = set()
    checkpoint = set()
    
    for line in log:
        if 'START' in line:
            undo.add(line[7:-1])
        elif 'COMMIT' in line:
            redo.add(line[8:-1])
        elif 'CKPT(' in line:
            temp = line[line.index('(') + 1:line.index(')')].split(',')
            checkpoint.update(temp)
            checkpoint = undo.difference(checkpoint)
    
    undo = undo.difference(redo)
    redo = redo.difference(checkpoint)

    print("Redo transactions:")
    for transaction in redo:
        print(transaction)
    
    print("\nUndo transactions:")
    for transaction in undo:
        print(transaction)

def main():
    with open("input.txt") as file:
        log = [line.strip() for line in file.readlines()]
    atomicRecovery(log)

if __name__ == '__main__':
    main()
