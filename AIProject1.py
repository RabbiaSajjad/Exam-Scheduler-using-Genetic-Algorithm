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




def readCourses(filename):
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
        return courseList

def readTeachers(filename):
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
                break
  #      print(f'Processed {line_count} lines.')

def readStudents(filename):
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
        return studentList

def readStudentCourses(filename,studentsList,courseList):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        flag=False
        for row in csv_reader:
            name=row[1]
            code=row[2]
    #        print(name,code)
            for y in studentsList:
                flag=False
                if(y.studentName == name):
                    i=0
                    while(i<y.courseCount):     
                        if (y.courseList[i].courseCode == code):
                            flag=True #This while loop checks if there are duplicates in this file, if there are 
                                        #multiple records of same student name and course code
                        i=i+1
                    if flag==False:
                        for x in courseList:
                            if(x.courseCode == code):
                                y.courseList.append(x)
                                y.courseCount=y.courseCount+1
                                break

            
            line_count=line_count+1
  #      print(f'Processed {line_count} lines.')
        for x in studentsList:
            print(x.studentName,x.courseCount)
            for y in x.courseList:
                print(y.courseCode)
        

courseList=readCourses("courses.csv")
readTeachers("teachers.csv")
studentList=readStudents("studentNames.csv")
readStudentCourses("studentCourse.csv",studentList,courseList)
