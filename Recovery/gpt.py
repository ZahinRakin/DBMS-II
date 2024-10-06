log = [
    "<START T1>",
    "<T1 A 1 2>",
    "<START T2>",
    "<COMMIT T1>",
    "<START T3>",
    "<T3 A 2 3>",
    "<START T4>",
    "<CKPT(T2,T3,T4)>",
    "<T2 B 10 20>",
    "<COMMIT T2>",
    "<START T5>",
    "<T5 D 1000 2000>",
    "<T4 C 100 200>",
    "<COMMIT T5>",
    "<START T6>",
    "<END CKPT>",
    "<T6 D 2000 3000>"
]

def process_log(log):
    committed_transactions = set()
    undo_transactions = set()
    active_transactions = set()
    
    # Phase 1: Analyze log
    for entry in log:
        if entry.startswith("<START "):
            transaction = entry.split()[1][:-1]
            active_transactions.add(transaction)
        elif entry.startswith("<COMMIT "):
            transaction = entry.split()[1][:-1]
            committed_transactions.add(transaction)
            if transaction in active_transactions:
                active_transactions.remove(transaction)
        elif entry.startswith("<CKPT"):
            # Parsing checkpoint information
            checkpoint_transactions = entry[entry.index('(') + 1:entry.index(')')].split(',')
            checkpoint_transactions = [t.strip() for t in checkpoint_transactions]
            # Undo transactions are the ones active at the checkpoint
            undo_transactions.update(set(checkpoint_transactions) - committed_transactions)

    # Phase 2: Redo committed transactions
    print("Redo the following transactions:")
    for entry in log:
        if any(f"<{t}" in entry for t in committed_transactions):
            print(entry)
    
    # Phase 3: Undo uncommitted transactions
    print("\nUndo the following transactions:")
    for entry in reversed(log):
        if any(f"<{t}" in entry for t in active_transactions):
            print(entry)

process_log(log)
