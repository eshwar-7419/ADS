# Function to create a new node
def create_node(value):
    return {"data": value, "left": None, "right": None}

# Function to insert a new value into the BST
def insert(root, value):
    if root is None:
        return create_node(value)
    if value < root["data"]:
        root["left"] = insert(root["left"], value)
    elif value > root["data"]:
        root["right"] = insert(root["right"], value)
    return root

# Function to search for a value in the BST
def search(root, value):
    if root is None:
        return False
    if root["data"] == value:
        return True
    elif value < root["data"]:
        return search(root["left"], value)
    else:
        return search(root["right"], value)

# Helper to find minimum node (used in deletion)
def find_min(root):
    while root and root["left"]:
        root = root["left"]
    return root

# Function to delete a value from the BST
def delete(root, value):
    if root is None:
        return None
    if value < root["data"]:
        root["left"] = delete(root["left"], value)
    elif value > root["data"]:
        root["right"] = delete(root["right"], value)
    else:
        # Node found
        if root["left"] is None:
            return root["right"]
        elif root["right"] is None:
            return root["left"]
        # Node with two children
        temp = find_min(root["right"])
        root["data"] = temp["data"]
        root["right"] = delete(root["right"], temp["data"])
    return root

# Traversals
def inorder(root):
    if root:
        inorder(root["left"])
        print(root["data"], end=" ")
        inorder(root["right"])

# def preorder(root):
#     if root:
#         print(root["data"], end=" ")
#         preorder(root["left"])
#         preorder(root["right"])

# def postorder(root):
#     if root:
#         postorder(root["left"])
#         postorder(root["right"])
#         print(root["data"], end=" ")

# ---------------- Main Program ----------------
root = None

print("Binary Search Tree Operations")
print("Options: 1:insert, 2:search, 3:delete, 4:inorder,5: exit")

while True:
    choice = input("\nEnter operation: ").lower()

    if choice == "1":
        print("Enter numbers to insert into tree :")
        nums=list(map(int,input().split()))
        for num in nums:
          root=insert(root,num)

    elif choice == "2":
        val = int(input("Enter value to search: "))
        if search(root, val):
            print(val, "is found in BST.")
        else:
            print(val, "is NOT found in BST.")

    elif choice == "3":
        val = int(input("Enter value to delete: "))
        root = delete(root, val)
        print(val, "deleted (if it existed).")

    elif choice == "4":
        print("Inorder traversal:", end=" ")
        inorder(root)
        print()

    elif choice == "5":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
