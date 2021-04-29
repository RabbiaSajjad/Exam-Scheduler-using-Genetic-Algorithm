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
                obj=Room(number)
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

class Room:
    def __init__(self,roomNo):
        self.roomNo=roomNo

class Exam:
    def __init__(self, course, invigilator, roomNo, day, timeSlot):
        self.course = course
        self.invigilator = invigilator
        self.roomNo = roomNo
        self.day = day
        self.timeSlot = timeSlot

class Day:
    def __init__(self):
        self.examsList = []
    
    def addExam(self, course, invigilator, roomNo, day, timeSlot):
        self.examsList.append(Exam(course, invigilator, roomNo, day, timeSlot))

class Schedule:
    def __init__(self, Controller):
        self.fitness = None             # if ZERO, that's our result
        self.daysList = [Day()] * 5         # list of days having list of exams

        totalRooms = len(Controller.roomList)
        totalCourses = len(Controller.courseList)
        totalTeachers = len(Controller.teacherList)
        print("TOTAL COURSES: ", totalCourses)
        # initialize random schedule for 5 days
        for day in range(5):  #Each Schedule for 5 days
            for timeSlot in range(4): #Each day divided into 4 time slots (Keeping duration = 2 hrs)
                for k in range(totalRooms): #Each timeslot will furthur have 10 rooms in which exams will be held
                    course = Controller.courseList[random.randint(0,totalCourses-1)].courseName
                    teacher = Controller.teacherList[random.randint(0,totalTeachers-1)].teacherName
                    roomNo = Controller.roomList[k].roomNo

                    self.daysList[day].addExam(course, teacher, roomNo, day, timeSlot)

                    #obj = Day(course, teacher, roomNo, day, timeSlot)
                    #self.days.append(obj)
                #timeSlot = timeSlot+1
            #j = j+1

    def makeSchedule():
        pass

class Population:
    def __init__(self, size, Controller):
        self.size = size
        self.scheduleList = [Schedule(Controller)] * size

    def displayPopulation(self):
        for schedule in range(self.size):          # Schedules
            print("----------------------------------Schedule # ", self.size, "----------------------------------")
            for day in range(5):            # days inside schedules
                print("\nDay: ", day)
                for exam in range(len(self.scheduleList[schedule].daysList[day].examsList)):       # exams in a day
                    print("Course: ", self.scheduleList[schedule].daysList[day].examsList[exam].course)
                    print("Teacher:", self.scheduleList[schedule].daysList[day].examsList[exam].invigilator)
                    print("Room No:", self.scheduleList[schedule].daysList[day].examsList[exam].roomNo)
                    print("Day:", self.scheduleList[schedule].daysList[day].examsList[exam].day)
                    print("Time Slot:", self.scheduleList[schedule].daysList[day].examsList[exam].timeSlot)

    # FITNESS STUFF

    def calculateFitness_Population(self, Controller):
        pass

    def calculateFitness_EveryCourseScheduled(self, Controller):
        pass

    def calculateFitness_StudentExamClash(self, Controller):
        pass

    


Controller = ControllerClass(None, None, None, None)
Controller.readCourses("courses.csv")
Controller.readTeachers("teachers.csv")
Controller.readStudents("studentNames.csv")
Controller.readStudentCourses("studentCourse.csv")
Controller.readRooms("rooms.csv")
population = Population(10, Controller)
population.displayPopulation()
#population.initializePopulation(Controller)
