import json
import random
import os

def generar_dataset_aleatorio(filename="dataset_aleatorio.json", n=50):
    items = []
    for i in range(1, n + 1):
        items.append({
            "id": f"X{i}",
            "cost": random.randint(1, 20),
            "volume": random.randint(1, 20)
        })
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=4)
    print(f"Dataset aleatorio '{filename}' generado exitosamente con {n} elementos.")

def generar_dataset_fijo(filename="dataset_fijo.json"):
    # Pre-defined array of items based on standard test cases
    # Using 10 items mapping exactly to the Excel image structure ideally, or a fixed 50 ones.
    # The image has 10 items. It's often best to test with the same data if possible to match expected output.
    # From Image: X1: (6, 4), X2: (6, 3), X3: (3, 11), X4: (6, 3)... Wait:
    # Image: 
    # X1: Cost=6, Vol=4
    # X2: Cost=6, Vol=3
    # X3: Cost=3, Vol=11
    # X4: Cost=6, Vol=3
    # X5: Cost=14, Vol=15
    # X6: Cost=10, Vol=9
    # X7: Cost=4, Vol=8
    # X8: Cost=10, Vol=6
    # X9: Cost=9, Vol=12
    # Oh wait, row 1 is Xi. Then we have X1 to X10. But there are only 9 columns? Wait:
    # Let me re-read the original image...
    # R1: X1 X2 X3 X4 X5 X6 X7 X8 X9 X10
    # Ci: 5  6  6  3  6  14 10 4  10 9
    # Vi: 8  4  3  11 3  15 9  8  6  12
    # This has 10 items. Let's use exactly these for the fixed dataset to allow 100% reproduction of the manual example.
    items = [
        {"id": "X1", "cost": 5, "volume": 8},
        {"id": "X2", "cost": 6, "volume": 4},
        {"id": "X3", "cost": 6, "volume": 3},
        {"id": "X4", "cost": 3, "volume": 11},
        {"id": "X5", "cost": 6, "volume": 3},
        {"id": "X6", "cost": 14, "volume": 15},
        {"id": "X7", "cost": 10, "volume": 9},
        {"id": "X8", "cost": 4, "volume": 8},
        {"id": "X9", "cost": 10, "volume": 6},
        {"id": "X10", "cost": 9, "volume": 12}
    ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=4)
    print(f"Dataset fijo '{filename}' generado exitosamente con {len(items)} elementos.")

def obtener_dataset_fijo():
    if not os.path.exists("dataset_fijo.json"):
        generar_dataset_fijo("dataset_fijo.json")
    with open("dataset_fijo.json", 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "aleatorio":
        generar_dataset_aleatorio()
    else:
        generar_dataset_fijo()
        generar_dataset_aleatorio()
