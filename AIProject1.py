import bisect
import sys
import collections
import collections.abc
import heapq
import operator
import os.path
import random
import math
import functools
import numpy as np
from itertools import chain, combinations
from queue import Queue
import csv


class ControllerClass:
    def __init__(self, studentList, courseList, teacherList, roomList):
        self.studentList=studentList
        self.courseList=courseList
        self.teacherList=teacherList
        self.roomList=roomList

    def getStudentList(self):
        return self.studentList
    
    def getCourseList(self):
        return self.courseList

    def getTeacherList(self):
        return self.teacherList
    
    def getRoomList(self):
        return self.roomList

    def readCourses(self,filename):
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            courseList=[]
            for row in csv_reader:
                code=row[0]
                name=row[1]
                obj=Course(code,name)
                courseList.append(obj)
                line_count=line_count+1
    #      print(f'Processed {line_count} lines.')
            
        self.courseList=courseList

    def readRooms(self,filename):
        with open(filename, 'r') as csv_file:
            roomList=[]
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                number=row[0]
                obj = Room(number)
                roomList.append(obj)      
    #      print(f'Processed {line_count} lines.')
            self.roomList=roomList

    def readTeachers(self,filename):
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            teacherList=[]
            for row in csv_reader:
                if(row):
                    name=row[0]
    #             print(name)
                    obj=Teacher(name)
                    teacherList.append(obj)
                    line_count=line_count+1
                else:
                    self.teacherList=teacherList
                    break

    def readStudents(self,filename):
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            studentList=[]
            for row in csv_reader:
                name=row[0]
                emptylist=[]
    #          print(name)
                obj=Student(name,emptylist,0)
                studentList.append(obj)
                line_count=line_count+1
    #       print(f'Processed {line_count} lines.')
            self.studentList=studentList

    def readStudentCourses(self,filename):
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            flag=False
            for row in csv_reader:
                name=row[1]
                code=row[2]
        #        print(name,code)
                for y in self.studentList:
                    flag=False
                    if(y.studentName == name):
                        i=0
                        while(i<y.courseCount):     
                            if (y.courseList[i].courseCode == code):
                                flag=True #This while loop checks if there are duplicates in this file,there are 
                                            #multiple records of same student name and course code
                            i=i+1
                        if flag==False:
                            for x in self.courseList:
                                if(x.courseCode == code):
                                    y.courseList.append(x)
                                    y.courseCount=y.courseCount+1
                                    break
                line_count=line_count+1             
    #      print(f'Processed {line_count} lines.')
            '''for x in self.studentList:
                print(x.studentName,x.courseCount)
                for y in x.courseList:
                    print(y.courseCode)'''

class Course:
    def __init__(self, courseCode, courseName):
        self.courseCode=courseCode
        self.courseName=courseName

class Student:
    def __init__(self, studentName, courseList, courseCount):
        self.studentName=studentName
        self.courseList=courseList  #This list contain instances of courses registered by the student
        self.courseCount=courseCount

class Teacher:
    def __init__(self, teacherName):
        self.teacherName=teacherName

#
# Schedule->Days->Rooms->examSlots->Exam
#

'''class Exam:
    def __init__(self, course, invigilator, roomNo, day):
        self.course = course
        self.invigilator = invigilator
'''

class ExamSlot:
    def __init__(self, studentsCapacity, invigilator, course):
        self.studentsCapacity = studentsCapacity
        self.students = []
        self.invigilator = invigilator
        self.course = course
        # 3 hour exam
        self.startingTime = {'hours': random.randint(9, 14), 'minutes': random.randrange(0, 59, 10)} # in 24 hour format (9am to 5pm) - starting time cannot be more than 2pm
        self.endingTime = {'hours': self.startingTime['hours'] + 3, 'minutes': self.startingTime['minutes']} # any minute multiple of 10 (eg. 9:10, 3:50)

    

class Room:

    def __init__(self, roomNo, studentsCapacity = 28, Controller = None):
        self.roomNo = roomNo
        self.examSlotList = []

        if Controller != None:
            totalCourses = len(Controller.courseList)
            totalTeachers = len(Controller.teacherList)
            
            check = True
            while check == True: 
                course = Controller.courseList[random.randint(0,totalCourses-1)].courseName
                teacher = Controller.teacherList[random.randint(0,totalTeachers-1)].teacherName
                check = self.addExamSlot(ExamSlot(studentsCapacity, teacher, course))


    def addExamSlot(self, examSlot):  # adds examSlot only if there is time available between 9am-5pm        
        # since only 2, 3 hour classes can be scheduled between 9am-5pm
        if len(self.examSlotList) == 0:
            self.examSlotList.append(examSlot)
            return True
        elif len(self.examSlotList) < 2:
            # check for clash/time-overlap
            for slot in self.examSlotList:
                slot1StartingTime = examSlot.startingTime['hours'] * 3600 + examSlot.startingTime['minutes'] * 60
                slot1EndingTime = examSlot.endingTime['hours'] * 3600 + examSlot.endingTime['minutes'] * 60
                slot2StartingTime = slot.startingTime['hours'] * 3600 + slot.startingTime['minutes'] * 60
                slot2EndingTime = slot.endingTime['hours'] * 3600 + slot.endingTime['minutes'] * 60

                # if timing not clashing
                if not ((slot2StartingTime >= slot1StartingTime and slot2StartingTime <= slot1EndingTime) or (slot2EndingTime >= slot1StartingTime and slot2EndingTime <= slot1EndingTime)):
                    self.examSlotList.append(examSlot)
                    return True
                else:
                    print("Clash")
                    return False
        else:
            print("Two exams in a day already")
            return False
                
class Day:
    def __init__(self, dayNo):
        self.dayNo = dayNo
        self.roomsList = []
    
    def addRoom(self, roomNo, studentsCapacity, Controller):
        room = Room(roomNo, studentsCapacity, Controller)
        self.roomsList.append(room)

    def canAddExam(self):
        for exam in examsList:
            pass

    def getAvailableExamSlot(self):
        pass

class Schedule:
    def __init__(self, Controller):
        self.fitness = None             # if ZERO, that's our result
        self.daysList = []              # list of days having list of exams

        for dayNo in range(5):
            self.daysList.append(Day(dayNo))

        totalRooms = len(Controller.roomList)

        # initialize random schedule for 5 days
        for day in range(5):  #Each Schedule for 5 days (0-4)
            for room in range(totalRooms):
                self.daysList[day].addRoom(Controller.roomList[room].roomNo, 28, Controller)

    def makeSchedule():
        pass

class Population:
    def __init__(self, size, Controller):
        self.size = size
        self.scheduleList = [Schedule(Controller)] * size

    def displayPopulation(self):
        for schedule in range(self.size):          # Schedules
            print("----------------------------------Schedule # ", schedule, "----------------------------------")
            for day in self.scheduleList[schedule].daysList:            # days inside schedules
                print("\nDay: ", day.dayNo)
                for room in day.roomsList:
                    print("\nRoom No. ", room.roomNo)
                    for examSlot in room.examSlotList:
                        print("\nCourse: ", examSlot.course, " Invigilator: ", examSlot.invigilator)

    # FITNESS STUFF
    '''
    Hard Constraints
    • An exam will be scheduled for each course.
    • A student is enrolled in at least 3 courses. A student cannot give more than 1 exam at a time.
    ~ Exam will not be held on weekends.
    ~ Each exam must be held between 9 am and 5 pm
    • Each exam must be invigilated by a teacher. A teacher cannot invigilate two exams at the same
    time.
    • A teacher cannot invigilate two exams in a row.
    '''

    def calculateFitness_Population(self, Controller):
        pass

    def calculateFitness_EveryCourseScheduled(self, Controller, schedule):
        pass

    def calculateFitness_StudentClash(self, Controller, schedule):
        pass

    def calculateFitness_InvigilatorClash(self, Controller, schedule):
        pass

    def calculateFitness_ConsecutiveInvigilations(self, Controller, schedule):
        pass

Controller = ControllerClass(None, None, None, None)
Controller.readCourses("courses.csv")
Controller.readTeachers("teachers.csv")
Controller.readStudents("studentNames.csv")
Controller.readStudentCourses("studentCourse.csv")
Controller.readRooms("rooms.csv")

population = Population(10, Controller)
population.displayPopulation()