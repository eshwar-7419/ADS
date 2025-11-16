#2nd version with operation like insertion and delete
# Simple Red-Black Tree in Python (Beginner-friendly)
# No classes, just functions and dictionaries

# Create NIL node (used instead of None for leaves)
NIL = {"key": None, "color": "B", "left": None, "right": None, "parent": None}

# Root of tree (starts empty)
root = NIL

# ------------------- Helper Functions -------------------

def create_node(key):
    """Create a new red node"""
    return {"key": key, "color": "R", "left": NIL, "right": NIL, "parent": None}

def left_rotate(x):
    """Perform a left rotation"""
    global root
    y = x["right"]
    x["right"] = y["left"]
    if y["left"] != NIL:
        y["left"]["parent"] = x
    y["parent"] = x["parent"]
    if x["parent"] == None:
        root = y
    elif x == x["parent"]["left"]:
        x["parent"]["left"] = y
    else:
        x["parent"]["right"] = y
    y["left"] = x
    x["parent"] = y

def right_rotate(x):
    """Perform a right rotation"""
    global root
    y = x["left"]
    x["left"] = y["right"]
    if y["right"] != NIL:
        y["right"]["parent"] = y
    y["parent"] = x["parent"]
    if x["parent"] == None:
        root = y
    elif x == x["parent"]["right"]:
        x["parent"]["right"] = y
    else:
        x["parent"]["left"] = y
    y["right"] = x
    x["parent"] = y

# ------------------- Insert Operations -------------------

def insert(key):
    """Insert a key into the Red-Black Tree"""
    global root
    node = create_node(key)
    y = None
    x = root

    while x != NIL and x["key"] is not None:
        y = x
        if node["key"] < x["key"]:
            x = x["left"]
        else:
            x = x["right"]

    node["parent"] = y
    if y == None:
        root = node
    elif node["key"] < y["key"]:
        y["left"] = node
    else:
        y["right"] = node

    node["left"] = NIL
    node["right"] = NIL
    node["color"] = "R"

    fix_insert(node)

def fix_insert(k):
    """Fix the tree after insertion"""
    global root
    while k["parent"] and k["parent"]["color"] == "R":
        if k["parent"] == k["parent"]["parent"]["left"]:
            u = k["parent"]["parent"]["right"]
            if u["color"] == "R":  # Case 1: uncle is red
                k["parent"]["color"] = "B"
                u["color"] = "B"
                k["parent"]["parent"]["color"] = "R"
                k = k["parent"]["parent"]
            else:
                if k == k["parent"]["right"]:  # Case 2: triangle
                    k = k["parent"]
                    left_rotate(k)
                # Case 3: line
                k["parent"]["color"] = "B"
                k["parent"]["parent"]["color"] = "R"
                right_rotate(k["parent"]["parent"])
        else:
            u = k["parent"]["parent"]["left"]
            if u["color"] == "R":
                k["parent"]["color"] = "B"
                u["color"] = "B"
                k["parent"]["parent"]["color"] = "R"
                k = k["parent"]["parent"]
            else:
                if k == k["parent"]["left"]:
                    k = k["parent"]
                    right_rotate(k)
                k["parent"]["color"] = "B"
                k["parent"]["parent"]["color"] = "R"
                left_rotate(k["parent"]["parent"])
    root["color"] = "B"

# ------------------- Delete Operations -------------------

def transplant(u, v):
    """Replace one subtree with another"""
    global root
    if u["parent"] == None:
        root = v
    elif u == u["parent"]["left"]:
        u["parent"]["left"] = v
    else:
        u["parent"]["right"] = v
    v["parent"] = u["parent"]

def tree_minimum(x):
    while x["left"] != NIL:
        x = x["left"]
    return x

def delete(key):
    """Delete a key from the tree"""
    global root
    z = root
    while z != NIL and z["key"] != key:
        if key < z["key"]:
            z = z["left"]
        else:
            z = z["right"]

    if z == NIL:
        print("Key not found!")
        return

    y = z
    y_original_color = y["color"]
    if z["left"] == NIL:
        x = z["right"]
        transplant(z, z["right"])
    elif z["right"] == NIL:
        x = z["left"]
        transplant(z, z["left"])
    else:
        y = tree_minimum(z["right"])
        y_original_color = y["color"]
        x = y["right"]
        if y["parent"] == z:
            x["parent"] = y
        else:
            transplant(y, y["right"])
            y["right"] = z["right"]
            y["right"]["parent"] = y
        transplant(z, y)
        y["left"] = z["left"]
        y["left"]["parent"] = y
        y["color"] = z["color"]
    if y_original_color == "B":
        fix_delete(x)

def fix_delete(x):
    """Fix tree after deletion"""
    global root
    while x != root and x["color"] == "B":
        if x == x["parent"]["left"]:
            s = x["parent"]["right"]
            if s["color"] == "R":
                s["color"] = "B"
                x["parent"]["color"] = "R"
                left_rotate(x["parent"])
                s = x["parent"]["right"]
            if s["left"]["color"] == "B" and s["right"]["color"] == "B":
                s["color"] = "R"
                x = x["parent"]
            else:
                if s["right"]["color"] == "B":
                    s["left"]["color"] = "B"
                    s["color"] = "R"
                    right_rotate(s)
                    s = x["parent"]["right"]
                s["color"] = x["parent"]["color"]
                x["parent"]["color"] = "B"
                s["right"]["color"] = "B"
                left_rotate(x["parent"])
                x = root
        else:
            s = x["parent"]["left"]
            if s["color"] == "R":
                s["color"] = "B"
                x["parent"]["color"] = "R"
                right_rotate(x["parent"])
                s = x["parent"]["left"]
            if s["right"]["color"] == "B" and s["left"]["color"] == "B":
                s["color"] = "R"
                x = x["parent"]
            else:
                if s["left"]["color"] == "B":
                    s["right"]["color"] = "B"
                    s["color"] = "R"
                    left_rotate(s)
                    s = x["parent"]["left"]
                s["color"] = x["parent"]["color"]
                x["parent"]["color"] = "B"
                s["left"]["color"] = "B"
                right_rotate(x["parent"])
                x = root
    x["color"] = "B"

# ------------------- Display -------------------

def inorder(node):
    """Inorder traversal"""
    if node != NIL and node["key"] is not None:
        inorder(node["left"])
        print(f"{node['key']}({node['color']})", end=" ")
        inorder(node["right"])

# ------------------- Main Menu -------------------

print("Red-Black Tree Operations")
print("Options: 1:insert, 2:delete , 3:inorder, 4: exit")

while True:
    choice = input("\nEnter operation: ").lower()

    if choice == "1":
        print("Enter numbers to insert into tree :")
        nums=list(map(int,input().split()))
        for num in nums:
          insert(num)

    elif choice == "2":
        val = int(input("Enter value to delete: "))
        delete(val)
        print(val, "deleted (if it existed).")

    elif choice == "3":
        print("Inorder traversal:", end=" ")
        inorder(root)
        print()

    elif choice == "4":
        print("Exiting program.")
        break

    else:
        print("Invalid choice! Try again.")
