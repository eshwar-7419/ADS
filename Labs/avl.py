#AVL Trees
def new_node(key):
    return {"key": key, "left": None, "right": None, "height": 1}

def height(node):
    return node["height"] if node else 0

def get_balance(node):
    return height(node["left"]) - height(node["right"]) if node else 0

def right_rotate(y):
    x = y["left"]
    T2 = x["right"]

    x["right"] = y
    y["left"] = T2

    y["height"] = 1 + max(height(y["left"]), height(y["right"]))
    x["height"] = 1 + max(height(x["left"]), height(x["right"]))

    return x

def left_rotate(x):
    y = x["right"]
    T2 = y["left"]

    y["left"] = x
    x["right"] = T2

    x["height"] = 1 + max(height(x["left"]), height(x["right"]))
    y["height"] = 1 + max(height(y["left"]), height(y["right"]))

    return y

def insert(root, key):
    if not root:
        return new_node(key)
    if key < root["key"]:
        root["left"] = insert(root["left"], key)
    else:
        root["right"] = insert(root["right"], key)

    root["height"] = 1 + max(height(root["left"]), height(root["right"]))
    balance = get_balance(root)

    if balance > 1 and key < root["left"]["key"]:
        return right_rotate(root)

    if balance < -1 and key > root["right"]["key"]:
        return left_rotate(root)

    if balance > 1 and key > root["left"]["key"]:
        root["left"] = left_rotate(root["left"])
        return right_rotate(root)

    if balance < -1 and key < root["right"]["key"]:
        root["right"] = right_rotate(root["right"])
        return left_rotate(root)

    return root

def min_value_node(node):
    while node["left"]:
        node = node["left"]
    return node

def delete(root, key):
    if not root:
        return root

    if key < root["key"]:
        root["left"] = delete(root["left"], key)
    elif key > root["key"]:
        root["right"] = delete(root["right"], key)
    else:
        if not root["left"]:
            return root["right"]
        elif not root["right"]:
            return root["left"]
        temp = min_value_node(root["right"])
        root["key"] = temp["key"]
        root["right"] = delete(root["right"], temp["key"])

    root["height"] = 1 + max(height(root["left"]), height(root["right"]))
    balance = get_balance(root)

    if balance > 1 and get_balance(root["left"]) >= 0:
        return right_rotate(root)

    if balance > 1 and get_balance(root["left"]) < 0:
        root["left"] = left_rotate(root["left"])
        return right_rotate(root)

    if balance < -1 and get_balance(root["right"]) <= 0:
        return left_rotate(root)

    if balance < -1 and get_balance(root["right"]) > 0:
        root["right"] = right_rotate(root["right"])
        return left_rotate(root)

    return root

def search(root, key):
    if not root or root["key"] == key:
        return root
    if key < root["key"]:
        return search(root["left"], key)
    return search(root["right"], key)

def inorder(root):
    if root:
        inorder(root["left"])
        print(root["key"], end=" ")
        inorder(root["right"])

        #-------main--------#

root = None

print("AVL Tree Operations")
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
            print(val, "is found in AVL Tree.")
        else:
            print(val, "is NOT found in AVL Tree.")

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
