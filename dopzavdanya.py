def is_subarray(nums1, nums2):
    i = 0
    for student in nums2:
        if i == len(nums1):
            break
        if (student["id"] == nums1[i]["id"] or        
                student["name"] == nums1[i]["name"] or    
                student["surname"] == nums1[i]["surname"]): 
            i += 1
    return i == len(nums1)


def input_students(group_name):
    students = []
    print(f"\nВведіть студентів групи {group_name} (для завершення введіть 'stop'):")
    while True:
        name = input("  Ім'я: ")
        if name.lower() == "stop":
            break
        surname = input("  Прізвище: ")
        student_id = input("  ID: ")
        students.append({
            "name": name,
            "surname": surname,
            "id": student_id,
            "group": group_name
        })
    return students


def input_subgroup():
    subgroup = []
    print("\nВведіть студентів підгрупи (для завершення введіть 'stop'):")
    print("Доступні групи: ir-11, ir-12, ir-13")
    while True:
        name = input("  Ім'я: ")
        if name.lower() == "stop":
            break
        surname = input("  Прізвище: ")
        student_id = input("  ID: ")
        group = input("  Група (ir-11/ir-12/ir-13): ")
        subgroup.append({
            "name": name,
            "surname": surname,
            "id": student_id,
            "group": group
        })
    return subgroup


ir13_students = input_students("ir-13")
subgroup = input_subgroup()

ir13_in_subgroup = []

for s in subgroup:
    if s["group"] == "ir-13":
        ir13_in_subgroup.append(s)
        
result = is_subarray(ir13_students, ir13_in_subgroup)


print("\n" + "=" * 40)
print("Студенти ir-13:", [f"{s['name']} {s['surname']}" for s in ir13_students])
print("Підгрупа:", [f"{s['name']} {s['surname']} ({s['group']})" for s in subgroup])
print(f"\nЧи є студенти ir-13 у підгрупі: {result}")

if result:
    print("Студенти ir-13 присутні у підгрупі в правильному порядку")
else:
    print("Студентів ir-13 немає у підгрупі або порядок порушений")
