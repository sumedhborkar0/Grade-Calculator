import pickle
import sys
import os
from colorama import Fore
from colorama import Style


class Assignments():
    loaded = False
    assignments_dict = {}
    color = None
    print(Style.BRIGHT)
    def __init__(self):
        self.sumPossible = 0
        self.sumEarned = 0
        print('\nEnter "STOP" to stop \n')
        while True:
            if not self.loaded:
                choice = input("Do you want to:\n"
                               "(1): Load an Old File?\n"
                               "(2): Add, Edit, or Delete an Assignment? \n"
                               "(3): Make a New File for the Current Assignments? \n"
                               "(4): Print Current Assignments Into Terminal?\n"
                               "(5): Calculate Grade?\n"
                               "(6): Sort File\n"
                               "(7): Change Text Color? ")
            if self.loaded:
                choice = input("Do you want to:\n"
                               "(1): Rename Current File?\n"
                               "(2): Add, Edit, or Delete an Assignment? \n"
                               "(3): Load Current Assignments Into Old File? \n"
                               "(4): Print Current Assignments Into Terminal?\n"
                               "(5): Calculate Grade?\n"
                               "(6): Sort File\n"
                               "(7): Change Text Color? ")

            if "stop" in choice.lower():
                sys.exit()
            try:
                choice = float(choice)

            except ValueError:
                pass

            if choice == 1 and not self.loaded:
                self.loadOldFile()
            elif choice == 1 and self.loaded:
                self.renameFile()
            elif choice == 2:
                print('\nEnter "end" to stop adding assignments')
                self.makeNewAssignment()
                print(self.assignments_dict)
            elif choice == 3 and not self.loaded:
                self.makeNewFile()
            elif choice == 3 and self.loaded:
                self.updateOldFile()
            elif choice == 4:
                self.printCurrentAssignments()
            elif choice == 5:
                self.calcGrade()
            elif choice == 6:
                self.sortFile()
            elif choice == 7:
                self.changeColor()
            elif isinstance(choice, str):
                print("\nPlease enter a number.\n")
            else:
                print("\nPlease enter a valid value!\n")

    def loadOldFile(self):
        while True:
            self.oldFileName = input("What was the old file called? ").lower()
            if self.oldFileName.lower() == "stop":
                self.__init__()
            else:
                try:
                    with open(f"{self.oldFileName}.txt", 'rb') as f:
                        self.assignments_dict = pickle.load(f)
                    print("\nLOADED\n")
                    self.loaded = True
                    break
                except FileNotFoundError:
                    print("\nPlease Enter A Valid File Name.\n")

    def updateOldFile(self):
        with open(f"{self.oldFileName}.txt", 'wb') as f:
            f.truncate(0)
            pickle.dump(self.assignments_dict, f)
            print("\n SAVED \n")

    def makeNewFile(self):
        self.newFileName = input("What do you want to call this file? ").lower()
        if self.newFileName.lower() == "stop":
            print("\nOk, the file was not saved.\n")
            self.__init__()
        else:
            with open(f"{self.newFileName}.txt", 'wb') as f:
                pickle.dump(self.assignments_dict, f)
            print("\n SAVED \n")

    def makeNewAssignment(self):
        def askPoints():
            self.pointsEarned = input("How many points did you earn? ")
            if "end" in self.pointsEarned.lower():
                self.__init__()
            while True:
                try:
                    self.pointsEarned = float(self.pointsEarned)
                    break
                except ValueError:
                    print("\nPlease enter a number.\n")
                    askPoints()
            self.pointsPossible = input("How many points were possible? ")
            if "end" in self.pointsPossible.lower():
                self.__init__()
            while True:
                try:
                    self.pointsPossible = float(self.pointsPossible)
                    break
                except ValueError:
                    print("\nPlease enter a number.\n")
                    askPoints()

        while True:
            changeChoice = input("\nDo you want to add, edit, or delete an assignment? ")
            if "add" in changeChoice.lower():
                while True:
                    name = input("What is the name of the assignment? ")
                    if name.lower() == "end":
                        self.__init__()
                    askPoints()
                    self.assignments_dict[name] = [self.pointsEarned, self.pointsPossible]
            elif "delete" in changeChoice.lower():
                while True:
                    oldName = input("What is the name of the assignment which you want to delete? ")
                    if oldName.lower() == "end":
                        self.__init__()
                    try:
                        self.fullNameFilled = False
                        self.fullOldName = ''
                        for key in self.assignments_dict.keys():
                            if key.startswith(oldName) and not self.fullNameFilled:
                                self.fullOldName = key
                                self.fullNameFilled = True
                            elif key.startswith(oldName) and self.fullNameFilled:
                                raise Exception()
                        self.assignments_dict[self.fullOldName]

                    except KeyError:
                        print("\nEnter a real assignment.\n")
                        continue
                    except:
                        print("\nTwo Assignments start with this name. Be more descriptive.\n")
                        continue
                    del self.assignments_dict[self.fullOldName]
                    break

            elif "edit" in changeChoice.lower():
                while True:
                    oldName = input("What is the name of the assignment which you want to edit? ")
                    if oldName.lower() == "end":
                        self.__init__()
                    try:
                        self.fullNameFilled = False
                        self.fullOldName = ''
                        for key in self.assignments_dict.keys():
                            if key.startswith(oldName) and not self.fullNameFilled:
                                self.fullOldName = key
                                self.fullNameFilled = True
                            elif key.startswith(oldName) and self.fullNameFilled:
                                raise Exception()
                        self.assignments_dict[self.fullOldName]

                    except KeyError:
                        print("\nEnter a real assignment.\n")
                        continue
                    except:
                        print("\nTwo Assignments start with this name. Be more descriptive.\n")
                        continue

                    name = input("What is the new name for this assignment? ")
                    if name.lower() == "end":
                        self.__init__()

                    self.assignments_dict[name] = self.assignments_dict.pop(self.fullOldName)
                    askPoints()
                    self.assignments_dict[name] = [self.pointsEarned, self.pointsPossible]
                    break
            elif "end" in changeChoice.lower():
                self.__init__()
            else:
                print('\nPlease choose either "add", "edit", or "delete".\n')

    def printCurrentAssignments(self):
        print("\n")
        for key in self.assignments_dict.keys():
            print(key, ":", self.assignments_dict[key])
        print("\n")

    def calcGrade(self):
        try:
            for elem in self.assignments_dict.values():
                self.sumEarned += elem[0]
                self.sumPossible += elem[1]
            grade = self.sumEarned / self.sumPossible
            roundedGrade = round(grade, 4) * 100
            print(f"\n{roundedGrade}%\n")
        except ZeroDivisionError:
            print("\nPlease enter your grades first!\n")

    def renameFile(self):
        self.changedName = input("\nWhat should the new file name be? ")
        if self.changedName.lower() == "stop":
            self.__init__()
            print("\nOk, the file name was not changed.\n")
        else:
            os.rename(f"{self.oldFileName}.txt", f"{self.changedName}.txt")
            print(f"\nChanged the file name from {self.oldFileName} to {self.changedName}\n")

    def changeColor(self):
        color = input("\nWhat Color Do You Want to Change the Text to? ")
        if "stop" not in color.lower():
            print(Style.BRIGHT)
            if "black" in color.lower():
                print(Fore.BLACK)
            elif "blue" in color.lower():
                print(Fore.BLUE)
            elif "cyan" in color.lower():
                print(Fore.CYAN)
            elif "green" in color.lower():
                print(Fore.GREEN)
            elif "magenta" in color.lower() or "purple" in color.lower() or "pink" in color.lower():
                print("\033[95m")
            elif "red" in color.lower():
                print(Fore.RED)
            elif "white" in color.lower():
                print(Fore.WHITE)
            elif "yellow" in color.lower():
                print(Fore.YELLOW)
            else:
                print("\nPlease enter a valid color.")
                self.changeColor()
        else:
            self.__init__()

    def sortFile(self):
        self.assignments_dict = dict(sorted(self.assignments_dict.items()))
        print("\nSORTED\n")
        self.__init__()


start = Assignments()
