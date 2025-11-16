# Create a new node as a dictionary
def make_node(value):
    return {"data": value, "left": None, "right": None}

# Insert level-order into binary tree
def insert_level_order(arr, i, n):
    if i >= n:
        return None

    node = make_node(arr[i])
    node["left"] = insert_level_order(arr, 2 * i + 1, n)
    node["right"] = insert_level_order(arr, 2 * i + 2, n)
    return node

# Traversals
def inorder(root):
    if root is None:
        return []
    return inorder(root["left"]) + [root["data"]] + inorder(root["right"])

def preorder(root):
    if root is None:
        return []
    return [root["data"]] + preorder(root["left"]) + preorder(root["right"])

def postorder(root):
    if root is None:
        return []
    return postorder(root["left"]) + postorder(root["right"]) + [root["data"]]

# Print tree sideways
def print_tree(root, space=0, level_space=5):
    if root is None:
        return

    space += level_space

    print_tree(root["right"], space)
    print()
    print(" " * (space - level_space) + str(root["data"]))
    print_tree(root["left"], space)


# -------- Main Program --------
print("Enter elements of the Binary Tree (space separated):")
arr = list(map(int, input().split()))

root = insert_level_order(arr, 0, len(arr))

print("\nBinary Tree Structure:")
print_tree(root)

print("\nInorder Traversal:", inorder(root))
print("Preorder Traversal:", preorder(root))
print("Postorder Traversal:", postorder(root))
