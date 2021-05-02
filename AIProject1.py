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
            empty=[]
            for row in csv_reader:
                code=row[0]
                name=row[1]
                obj=Course(code,name, empty,0)
                courseList.append(obj)
                line_count=line_count+1
    #      print(f'Processed {line_count} lines.')
            
        self.courseList=courseList

    def readRooms(self,filename):
        with open(filename, 'r') as csv_file:
            roomList = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                number=row[0]
                obj = Room(number, 28)
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
                    # print(name)
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
                # print(name)
                obj=Student(name,emptylist,0)
                studentList.append(obj)
                line_count=line_count+1
                # print(f'Processed {line_count} lines.')
            self.studentList=studentList
            

    def readStudentCourses(self,filename):
        students=[]
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
                                    x.count=x.count+1
                                    y.courseList.append(x)
                                    y.courseCount=y.courseCount+1
                                    
                                    break
                line_count=line_count+1   
    #      print(f'Processed {line_count} lines.')
            for x in self.courseList:
                print(x.courseName, x.count)
               


class Course:
    def __init__(self, courseCode, courseName, studentsRegistered,count):
        self.courseCode=courseCode
        self.courseName=courseName
        self.studentsRegistered=studentsRegistered
        self.count=count
        self.flag=False #exam scheduled or not

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

class Room:

    def __init__(self, roomNo, studentsCapacity = 28):
        self.roomNo = roomNo
        self.studentsCapacity = studentsCapacity
            
            
class ExamSlot:
    def __init__(self, invigilator, course, studentList, Controller):
        self.roomsList = []
        self.students = []
        self.invigilator = invigilator
        self.course = course
        # 3 hour exam
        self.startingTime = {'hours': random.randint(9, 14), 'minutes': random.randrange(0, 59, 10)} # in 24 hour format (9am to 5pm) - starting time cannot be more than 2pm
        self.endingTime = {'hours': self.startingTime['hours'] + 3, 'minutes': self.startingTime['minutes']} # any minute multiple of 10 (eg. 9:10, 3:50)

        if self.startingTime['hours'] == 14:
            self.startingTime['minutes'] = 0
            self.endingTime['minutes'] = 0

        for x in studentList:
            for y in x.courseList:
                if(y.courseName == course.courseName):
                    self.students.append(x)
                   

        # ----randomly allocates series of rooms----
        roomsNeeded = 0
        if len(self.students) % 28 == 0:
            roomsNeeded = int(len(self.students) / 28)
        else:
            roomsNeeded = int(len(self.students) / 28) + 1

        randomNo = 0
        randomNo = random.randint(0, len(Controller.roomList) - roomsNeeded) # we subtract roomsNeeded to keep allocation in range 

        while roomsNeeded != 0:
            self.roomsList.append(Controller.roomList[randomNo].roomNo)
            #print("ROOOM ", Controller.roomList[randomNo].roomNo)
            randomNo += 1
            roomsNeeded -= 1


    def addRoom(self, roomNo, Courses,teachers,students,studentsCapacity):
        room = Room(roomNo, Courses, teachers,students,studentsCapacity)
        self.roomsList.append(room)

                
class Day:
    def __init__(self, dayNo, courseList, teacherList, studentList):
        self.dayNo = dayNo
        self.examSlotList = []
        self.teachersOnDuty = []
        
    def addExamSlot(self, teacherList, course, studentList, Controller):  # adds examSlot only if there is time available between 9am-5pm        
        
        invigilator = random.choice(teacherList).teacherName
        self.teachersOnDuty.append(invigilator)
        self.examSlotList.append(ExamSlot(invigilator, course, studentList, Controller))

class Schedule:
    def __init__(self, Controller):

        roomList = Controller.roomList
        studentList = Controller.studentList
        courseList = Controller.courseList
        teacherList = Controller.teacherList          # NEW COPIES OF LISTS

        self.daysList = []                            # list of days having list of exams
        for dayNo in range(5): self.daysList.append(Day(dayNo, courseList, teacherList, studentList))

        # initialize random schedule for 5 days
        self.makeRandSchedule(Controller, teacherList, courseList, studentList)
    
    def makeRandSchedule(self, Controller, teacherList, courseList, studentList): 
        for course in range(len(Controller.courseList)):
            random.choice(self.daysList).addExamSlot(teacherList, random.choice(Controller.courseList), studentList, Controller)


class Individual:

    def __init__(self, chromosome, Controller):
        self.chromosome = chromosome 
        self.fitness = 0

    def calculateFitness(self, Controller):
        self.calculateFitness_StudentClash(Controller)
        self.calculateFitness_EveryCourseScheduled(Controller)
        self.calculateFitness_InvigilatorClash(Controller)
        self.calculateFitness_ConsecutiveInvigilations(Controller)

        return self.fitness

    def calculateFitness_EveryCourseScheduled(self, Controller):  # for each course not present in schedule fitness += 1
        coursesInSchedule = []
        for day in self.chromosome.daysList:
            for exam in day.examSlotList:
                coursesInSchedule.append(exam.course.courseName)

        coursesInCourseList = []
        for course in Controller.courseList:
            coursesInCourseList.append(course.courseName)
        
        for course in coursesInCourseList:
            if course not in coursesInSchedule:
                self.fitness += 1


    def calculateFitness_StudentClash(self, Controller):
        for day in self.chromosome.daysList:
            examSchedule=[] #This list contains all exams scheduled on a particular day
            for exam in day.examSlotList:
                examSchedule.append(exam)
            for exam in day.examSlotList:
                for x in exam.students:
                    print(x.studentName," on day ",day.dayNo)
                    check=self.checkTimings(examSchedule, x.courseList)
                    self.fitness+=check

                   


    def checkTimings(self,exams, courses):
        count=0
        course1=course2=''
        for exam in exams:
            if(exam.course in courses):
                count=count+1
                if (count==1):
                    course1=exam.course.courseName
                    
                
                elif(count==2):
                    course2=exam.course.courseName
                                      
                
        print("Number of exams in a day: ",count)
        if count > 2:
            print("Two exams already")
            return (count-2) #More than 2 exams scheduled in a day of a student
        else:
            return 0 #Clash Free

    def calculateFitness_InvigilatorClash(self, Controller):
        for day in self.chromosome.daysList:           
            for exam in day.examSlotList:
                count=0
                invigilator=exam.invigilator
                for x in day.examSlotList:
                    if(invigilator==x.invigilator):
                        count=count+1
                    if(count>1): 
                        print("Invigilator Clash: ", exam.invigilator, " on day ",day.dayNo)         
                        self.fitness+=1
                        break
                    
                continue

                

    def calculateFitness_ConsecutiveInvigilations(self, Controller):
        pass #We don't need this

class Population:
    def __init__(self, size, Controller):
        self.size = size
        self.population = [Individual(Schedule(Controller), Controller)] * size     # each schedule is a chromosome

    def displayPopulation(self):
        for schedule in range(self.size):          # Schedules
            print("----------------------------------Schedule # ", schedule, "----------------------------------")
            for day in self.population[schedule].chromosome.daysList:            # days inside schedules
                print("\nDay: ", day.dayNo)
                for examSlot in day.examSlotList:
                    print("\nCourse: ", examSlot.course.courseName, " Invigilator: ", examSlot.invigilator)
                    print("Time: ", examSlot.startingTime, " - ", examSlot.endingTime)
                    print("Students: ")
                    for x in examSlot.students:
                        print(x.studentName, end=", ")
                    print("Rooms: ", examSlot.roomsList)
        
        print("Calculate fitness: ",self.population[0].calculateFitness(Controller))


    def selectIndividual(self,Controller): #Selects Individuals with minimum number of conflicts
        min1=min2=self.population[0].calculateFitness()
        Individual1=self.population[0]
        Individual2=self.population[0]
        for schedule in range(self.size): 
            for x in self.population[schedule]:
                if (min1> x.calculateFitness(Controller)):
                    min1=x.calculateFitness(Controller)
                    Individual1=x
                elif (min2> x.calculateFitness(Controller)):
                    min2=x.calculateFitness(Controller)
                    Individual2=x
     
        
    # FITNESS STUFF
    '''
    Hard Constraints
    • An exam will be scheduled for each course. (Done)
    • A student is enrolled in at least 3 courses. A student cannot give more than 1 exam at a time.
    ~ Exam will not be held on weekends. (Done)
    ~ Each exam must be held between 9 am and 5 pm (done)
    • Each exam must be invigilated by a teacher. A teacher cannot invigilate two exams at the same
    time. (Indirectly Done :D)

    • A teacher cannot invigilate two exams in a row. (Indirectly Done :D)
    '''

    

Controller = ControllerClass(None, None, None, None)
Controller.readCourses("courses.csv")
Controller.readTeachers("teachers.csv")
Controller.readStudents("studentNames.csv")
Controller.readStudentCourses("studentCourse.csv")
Controller.readRooms("rooms.csv")

population = Population(10, Controller)
population.displayPopulation()