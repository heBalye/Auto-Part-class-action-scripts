with open("./test/example.txt", "r") as text:
    VIN_string = text.read()
# print(len(VIN.split(";")))
# print(VIN.count(";"))
# print(VIN)

from CleanVIN import ValidationProcess

VIN = ValidationProcess(VIN_string, 10)
print(VIN.getAll())
