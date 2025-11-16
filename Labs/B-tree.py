#B-Trees
# The degree 't' is a crucial parameter for the B-Tree structure.
# A node must have between t-1 and 2t-1 keys.
T_VALUE = 2

# --- BTree Node Structure (Represented as a Dictionary) ---
# A node is a dictionary with the following keys:
# 't': The minimum degree (order/2)
# 'keys': List of keys in the node
# 'children': List of child nodes (dictionaries)
# 'leaf': Boolean indicating if the node is a leaf

# Function to create a new BTreeNode dictionary
def create_b_tree_node(t, is_leaf=False):
    return {
        't': t,
        'keys': [],
        'children': [],
        'leaf': is_leaf
    }

# --- BTree Structure (Represented by the root node and T_VALUE) ---
# The B-Tree itself is managed by the root node and the global T_VALUE.

# Initialize the BTree (Root is a leaf)
B_TREE_ROOT = create_b_tree_node(T_VALUE, is_leaf=True)

# ----------------------------------------------------------------------
# ---- SEARCH FUNCTION ----
# ----------------------------------------------------------------------
def search(key, node=None):
    if node is None:
        node = B_TREE_ROOT

    i = 0
    # Find the first key greater than or equal to 'key'
    while i < len(node['keys']) and key > node['keys'][i]:
        i += 1

    # Check if key is found at the current index
    if i < len(node['keys']) and node['keys'][i] == key:
        return True

    # If it's a leaf, key is not in the tree
    if node['leaf']:
        return False

    # Recurse into the appropriate child
    return search(key, node['children'][i])

# ----------------------------------------------------------------------
# ---- INSERT HELPERS ----
# ----------------------------------------------------------------------
def split_child(parent, index, child):
    t = T_VALUE
    # Create a new sibling node
    new_child = create_b_tree_node(t, child['leaf'])

    # Move the median key from 'child' to 'parent'
    parent['keys'].insert(index, child['keys'][t - 1])

    # Insert the new child node into the parent's children list
    parent['children'].insert(index + 1, new_child)

    # Move keys from the right half of 'child' to 'new_child'
    new_child['keys'] = child['keys'][t:]

    # Keep only the left half of the keys in 'child'
    child['keys'] = child['keys'][:t - 1]

    # If not a leaf, move children pointers as well
    if not child['leaf']:
        new_child['children'] = child['children'][t:]
        child['children'] = child['children'][:t]

def insert_non_full(node, key):
    t = T_VALUE
    i = len(node['keys']) - 1

    if node['leaf']:
        # Insert key into leaf node
        node['keys'].append(None)
        while i >= 0 and key < node['keys'][i]:
            node['keys'][i + 1] = node['keys'][i]
            i -= 1
        node['keys'][i + 1] = key
    else:
        # Find the appropriate child to descend into
        while i >= 0 and key < node['keys'][i]:
            i -= 1
        i += 1 # i is the index of the child to descend into

        # Check if the child is full, and split if necessary
        if len(node['children'][i]['keys']) == (2 * t) - 1:
            split_child(node, i, node['children'][i])

            # After split, key might belong to the new sibling (index i+1)
            if key > node['keys'][i]:
                i += 1

        # Recurse into the appropriate child
        insert_non_full(node['children'][i], key)

# ----------------------------------------------------------------------
# ---- INSERT FUNCTION ----
# ----------------------------------------------------------------------
def insert(key):
    global B_TREE_ROOT
    root = B_TREE_ROOT
    t = T_VALUE

    if len(root['keys']) == (2 * t) - 1:
        # Root is full, create a new root
        new_root = create_b_tree_node(t, is_leaf=False)
        new_root['children'].insert(0, root)

        # Split the old root and make the new root the parent
        split_child(new_root, 0, root)

        # Update the global root pointer
        B_TREE_ROOT = new_root

        # Insert the key into the new (non-full) root
        insert_non_full(new_root, key)
    else:
        insert_non_full(root, key)

# ----------------------------------------------------------------------
# ---- DELETE HELPERS ----
# ----------------------------------------------------------------------

# Helper to find the predecessor key
def get_pred(node, idx):
    cur = node['children'][idx]
    while not cur['leaf']:
        cur = cur['children'][-1]
    return cur['keys'][-1]

# Helper to find the successor key
def get_succ(node, idx):
    cur = node['children'][idx + 1]
    while not cur['leaf']:
        cur = cur['children'][0]
    return cur['keys'][0]

# Helper to merge a child with its next sibling
def merge(node, idx):
    child = node['children'][idx]
    sibling = node['children'][idx + 1]

    # Move the key from the parent to the end of the child's keys
    child['keys'].append(node['keys'].pop(idx))

    # Move all keys from the sibling to the child
    child['keys'].extend(sibling['keys'])

    # Move all children from the sibling to the child
    if not child['leaf']:
        child['children'].extend(sibling['children'])

    # Remove the sibling from the parent's children list
    node['children'].pop(idx + 1)

# Helper to borrow a key from the previous sibling
def borrow_prev(node, idx):
    child = node['children'][idx]
    sibling = node['children'][idx - 1]

    # Move key from parent to the start of child's keys
    child['keys'].insert(0, node['keys'][idx - 1])

    # Move key from end of sibling to parent
    node['keys'][idx - 1] = sibling['keys'].pop()

    # If not a leaf, move the last child pointer from sibling to child
    if not child['leaf']:
        child['children'].insert(0, sibling['children'].pop())

# Helper to borrow a key from the next sibling
def borrow_next(node, idx):
    child = node['children'][idx]
    sibling = node['children'][idx + 1]

    # Move key from parent to the end of child's keys
    child['keys'].append(node['keys'][idx])

    # Move key from start of sibling to parent
    node['keys'][idx] = sibling['keys'].pop(0)

    # If not a leaf, move the first child pointer from sibling to child
    if not child['leaf']:
        child['children'].append(sibling['children'].pop(0))

# Helper to ensure the child node at index 'idx' has at least 't' keys
def fill(node, idx):
    t = T_VALUE

    # Case 1: Borrow from previous sibling (if it has enough keys)
    if idx != 0 and len(node['children'][idx - 1]['keys']) >= t:
        borrow_prev(node, idx)
    # Case 2: Borrow from next sibling (if it has enough keys)
    elif idx != len(node['children']) - 1 and len(node['children'][idx + 1]['keys']) >= t:
        borrow_next(node, idx)
    # Case 3: Merge with a sibling
    else:
        if idx != len(node['children']) - 1:
            # Merge with next sibling
            merge(node, idx)
        else:
            # Merge with previous sibling
            merge(node, idx - 1)

# ----------------------------------------------------------------------
# ---- DELETE CORE FUNCTION ----
# ----------------------------------------------------------------------
def _delete(node, key):
    t = T_VALUE

    if key in node['keys']:
        idx = node['keys'].index(key)

        if node['leaf']:
            # Case 1: Key is in a leaf node
            node['keys'].pop(idx)
        else:
            # Case 2: Key is in an internal node

            # Case 2a: Left child has at least 't' keys
            if len(node['children'][idx]['keys']) >= t:
                pred = get_pred(node, idx)
                node['keys'][idx] = pred
                _delete(node['children'][idx], pred)
            # Case 2b: Right child has at least 't' keys
            elif len(node['children'][idx + 1]['keys']) >= t:
                succ = get_succ(node, idx)
                node['keys'][idx] = succ
                _delete(node['children'][idx + 1], succ)
            # Case 2c: Both children have t-1 keys
            else:
                merge(node, idx)
                _delete(node['children'][idx], key)
    else:
        if node['leaf']:
            # Key not found
            return

        # Find the child index to descend into
        idx = 0
        while idx < len(node['keys']) and key > node['keys'][idx]:
            idx += 1

        child_to_descend = node['children'][idx]

        # Case 3: Ensure child has at least 't' keys before descending
        if len(child_to_descend['keys']) < t:
            fill(node, idx)

        # After fill(), the structure might have changed (e.g., merge)
        # We need to determine the correct child to descend into *after* fill.

        # If fill resulted in a merge with the right sibling, the key might now be in a merged node
        if idx > len(node['keys']): # This means a merge happened and the original child index 'idx' is now gone
            _delete(node['children'][idx - 1], key)
        # If the key is now greater than the parent key at idx (due to borrow/merge), go right
        elif idx < len(node['keys']) and key > node['keys'][idx]:
            _delete(node['children'][idx + 1], key)
        else:
            # Otherwise, descend into the (potentially modified) child at index 'idx'
            _delete(node['children'][idx], key)


# ----------------------------------------------------------------------
# ---- DELETE FUNCTION (Public Interface) ----
# ----------------------------------------------------------------------
def delete(key):
    global B_TREE_ROOT
    _delete(B_TREE_ROOT, key)

    # If root becomes empty and is not a leaf, its first child becomes the new root
    if len(B_TREE_ROOT['keys']) == 0 and not B_TREE_ROOT['leaf']:
        B_TREE_ROOT = B_TREE_ROOT['children'][0]

# ----------------------------------------------------------------------
# ---- DISPLAY FUNCTIONS ----
# ----------------------------------------------------------------------
def display_node(node, level=0):
    print("Level", level, "Keys:", node['keys'])
    for child in node['children']:
        display_node(child, level + 1)

def display_b_tree():
    print("\nB-Tree Structure:")
    display_node(B_TREE_ROOT)
    print()

# ----------------------------------------------------------------------
# ---- USER INPUT MENU ----
# ----------------------------------------------------------------------

# Re-initialize the root before starting the menu
B_TREE_ROOT = create_b_tree_node(T_VALUE, is_leaf=True)
print("B-Tree Operations")
print("Options: 1:insert, 2:search, 3:delete, 4:display, 5: exit")
while True:
    choice = input("\nEnter operation: ").lower()

    if choice == "1":
        print("Enter numbers to insert into tree :")
        nums=list(map(int,input().split()))
        for num in nums:
          insert(num) # Corrected: only pass num, operate on global B_TREE_ROOT

    elif choice == "2":
        val = int(input("Enter value to search: "))
        if search(val): # Corrected: only pass val, search starts from global B_TREE_ROOT
            print(val, "is found in B-Tree.")
        else:
            print(val, "is NOT found in B-Tree.")

    elif choice == "3":
        val = int(input("Enter value to delete: "))
        delete(val) # Corrected: only pass val, operate on global B_TREE_ROOT
        print(val, "deleted (if it existed).")

    elif choice == "4":
        display_b_tree()

    elif choice == "5":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
