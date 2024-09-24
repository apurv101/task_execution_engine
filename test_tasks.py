# test_tasks.py

# A list of simple task descriptions for QuickBooks automation testing
test_tasks = [
    "Create a new invoice for customer John Doe for $500.",
    "Record a payment received from customer Jane Smith for invoice #1234.",
    "Add a new expense for office supplies costing $100.",
    "Generate a profit and loss report for the last quarter.",
    "Create a new customer named Acme Corporation.",
    "Update the inventory to reflect the purchase of 50 units of product XYZ.",
    "Set up a recurring transaction for monthly rent of $2,000.",
    "Send an invoice reminder to customer ABC Company for overdue invoice #5678.",
    "Reconcile the bank statement for the current month.",
    "Export the customer list to a CSV file.",
    "Delete an incorrect transaction from the ledger.",
    "Modify the terms for vendor XYZ Supplies to Net 30.",
    "Apply a discount of 10% to invoice #4321 for customer Global Tech.",
    "Create a journal entry to adjust the prepaid expenses account.",
    "Generate an accounts receivable aging report.",
    "Add a new payment method called 'Digital Wallet'.",
    "Issue a refund receipt to customer Emily Clark for $75.",
    "Customize the invoice template to include the company logo.",
    "Backup the company file to an external drive.",
    "Change the company address in the account settings."
]

# Example usage:
if __name__ == "__main__":
    for idx, task in enumerate(test_tasks, start=1):
        print(f"Task {idx}: {task}")
