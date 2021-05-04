import bisect
import sys
import collections
import collections.abc
import operator
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
                
            
        self.courseList=courseList

    def readRooms(self,filename):
        with open(filename, 'r') as csv_file:
            roomList = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                number=row[0]
                obj = Room(number, 28)
                roomList.append(obj)      
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
            i=0
            for x in self.courseList:
                if x.count == 0:
                    self.courseList.pop(i)
                i=i+1
            for x in self.courseList:    
                print(x.courseName, x.count)
                
                
               


class Course:
    def __init__(self, courseCode, courseName, studentsRegistered,count):
        self.courseCode=courseCode
        self.courseName=courseName
        self.studentsRegistered=studentsRegistered
        self.count=count
        self.flag=False #exam scheduled or not
        self.gene=""

    

class Student:

    def __init__(self, studentName, courseList, courseCount):
        self.studentName=studentName
        self.courseList=courseList  #This list contain instances of courses registered by the student
        self.courseCount=courseCount
        

class Teacher:
    def __init__(self, teacherName):
        self.teacherName=teacherName
        self.gene=""

#
# Schedule->Days->Rooms->examSlots->Exam
#

class Room:

    def __init__(self, roomNo, studentsCapacity = 28):
        self.roomNo = roomNo
        self.studentsCapacity = studentsCapacity
        self.gene=""
            
            
class ExamSlot:
    def __init__(self, invigilator, course, studentList, Controller):
        self.roomsList = []
        self.students = []
        self.invigilator = []
        self.course = course
        
        # 3 hour exam
        slot = random.randint(0, 1)
        if slot == 0:
            self.startingTime = {'hours': 9, 'minutes': 0} # in 24 hour format (9am to 5pm) - starting time cannot be more than 2pm
            self.endingTime = {'hours': 12, 'minutes': 0} # any minute multiple of 10 (eg. 9:10, 3:50)
            self.Timegene="0"
        if slot == 1:
            self.startingTime = {'hours': 2, 'minutes': 0} # in 24 hour format (9am to 5pm) - starting time cannot be more than 2pm
            self.endingTime = {'hours': 5, 'minutes': 0} # any minute multiple of 10 (eg. 9:10, 3:50)
            self.Timegene="1"

        # Alternative random slot generating code:
        """ self.startingTime = {'hours': random.randint(9, 14), 'minutes': random.randrange(0, 59, 10)} # in 24 hour format (9am to 5pm) - starting time cannot be more than 2pm
        self.endingTime = {'hours': self.startingTime['hours'] + 3, 'minutes': self.startingTime['minutes']} # any minute multiple of 10 (eg. 9:10, 3:50)
        if self.startingTime['hours'] == 14:
            self.startingTime['minutes'] = 0
            self.endingTime['minutes'] = 0
        """
        

        for x in studentList:
            for y in x.courseList:
                if(y.courseName == course.courseName):
                    self.students.append(x)
                   

        # ----randomly allocates series of rooms----
        roomsNeeded = 0
        if len(self.students) <= 28:
            roomsNeeded = 1
            
        else:
            roomsNeeded = int(len(self.students) / 28) + 1
            

        randomNo = 0
        randomNo = random.randint(0, len(Controller.roomList) - roomsNeeded) # we subtract roomsNeeded to keep allocation in range 
        rand = random.randint(0, len(Controller.teacherList)-1)
        while roomsNeeded != 0:
            self.roomsList.append(Controller.roomList[randomNo])
            self.invigilator.append(Controller.teacherList[rand])
            rand = random.randint(0, len(Controller.teacherList)-1)
            randomNo += 1
            roomsNeeded -= 1


    def addRoom(self, roomNo, Courses,teachers,students,studentsCapacity):
        room = Room(roomNo, Courses, teachers,students,studentsCapacity)
        self.roomsList.append(room)

                
class Day:
    def __init__(self, dayNo, courseList, teacherList, studentList,gene):
        self.dayNo = dayNo
        self.examSlotList = []
        self.teachersOnDuty = []
        self.gene=gene

        
    def addExamSlot(self, teacherList, course, studentList, Controller):  # adds examSlot only if there is time available between 9am-5pm        
        
        invigilator = random.choice(teacherList)
        self.teachersOnDuty.append(invigilator)
        self.examSlotList.append(ExamSlot(invigilator, course, studentList, Controller))

class Schedule:
    def __init__(self, Controller, courseList, teacherList):

        self.roomList = Controller.roomList
        self.studentList = Controller.studentList
        self.courseList = courseList
        self.teacherList=teacherList
        self.examScheduled=[]
        self.daysList = []                            # list of days having list of exams
        
        
        for dayNo in range(8): 
            size=5
            bitLength=math.log2(size)
            n =math.ceil(bitLength)                       
            for i in  range(0,size):
                b = bin(i)[2:]
                l = len(b)
                b = str(0) * (n - l) + b
            self.daysList.append(Day(dayNo, self.courseList, self.teacherList, self.studentList,b))

        # initialize random schedule for 5 days
        self.makeRandSchedule(Controller, self.teacherList, self.courseList, self.studentList)

        

        
    
    def makeRandSchedule(self, Controller, teacherList, courseList, studentList): 
        self.examScheduled=[]
        for course in range(len(Controller.courseList)):
            Course=random.choice(Controller.courseList)
            while (Course in self.examScheduled):
                Course=random.choice(Controller.courseList)
            self.examScheduled.append(Course)  
       #     print("TRue")  
            random.choice(self.daysList).addExamSlot(teacherList, Course, studentList, Controller)


class Individual:

    def __init__(self, chromosome, Controller):
        self.chromosome = chromosome 
        self.fitness = 0

       

    def calculateFitness(self, Controller):
        self.fitness=self.calculateFitness_EveryCourseScheduled(Controller)
    #    print("Courses Fitness: ",self.fitness)
        self.fitness+=self.calculateFitness_StudentClash(Controller)
     #   print("Student Fitness: ",self.fitness)
        self.fitness+=self.calculateFitness_InvigilatorClash(Controller)
      #  print("Invigilator Fitness: ",self.fitness)
   #     self.fitness+=self.calculateFitness_ConsecutiveInvigilations(Controller)

        return self.fitness

    def calculateFitness_EveryCourseScheduled(self, Controller):  # for each course not present in schedule fitness += 1
        fitness=0
        coursesInSchedule = []
        for day in self.chromosome.daysList:
            for exam in day.examSlotList:
                coursesInSchedule.append(exam.course.courseName)

        coursesInCourseList = []
        for course in Controller.courseList:
            coursesInCourseList.append(course.courseName)
        
        for course in coursesInCourseList:
            if course not in coursesInSchedule:
                fitness += 1

        return fitness

    def calculateFitness_StudentClash(self, Controller):
        fitness=0
        count=0
        for day in self.chromosome.daysList:
            examSchedule=[] #This list contains all exams scheduled on a particular day
            for exam in day.examSlotList:
                examSchedule.append(exam)
            for exam in day.examSlotList:
                for x in exam.students:
                    check=self.checkTimings(examSchedule, x.courseList)
                    if(check!=0):
                        fitness+=1
                        count+=1
                      #  print(x.studentName," on day ",day.dayNo," have clashes count",check)
                  #  if(check!=0):
                        #print(x.studentName," on day ",day.dayNo," have clashes count",check)
 #       print("COUNT: ",count)    
        return fitness
                   


    def checkTimings(self,exams, courses):
        count=0
        course1=course2=''
        for exam in exams:
            if(exam.course in courses):
                count=count+1
               
                                      
             
        if count > 2:
            return (count-2) #More than 2 exams scheduled in a day of a student
        else:
            return 0 #Clash Free

    def calculateFitness_InvigilatorClash(self, Controller):
        fitness=0
       
        for day in self.chromosome.daysList: 
            invigilatorList=[] #All invigilators in a day  
                   
            for exam in day.examSlotList:           
                for y in exam.invigilator:
                    invigilatorList.append(y.teacherName)

            for exam in day.examSlotList:
                for z in exam.invigilator:
                    count=0 
                    if(z.teacherName in invigilatorList):
                        count=count+1
                    if(count>1): 
        #                print("Invigilator Clash: ", z.teacherName, " on day ",day.dayNo)         
                        self.fitness+=1
                        break
                    
                #continue
        return fitness
                

    def calculateFitness_ConsecutiveInvigilations(self, Controller):
        pass #We don't need this


#


    def displayIndividual(self):
        for day in self.chromosome.daysList:
            print("\n\nDay: ", day.dayNo)
            for examSlot in day.examSlotList:
                print("\n\nCourse: ", examSlot.course.courseName)
                for y in examSlot.invigilator:
                    print("Invigilator: ", y.teacherName)
                print("Time: ", examSlot.startingTime, " - ", examSlot.endingTime)
                print("Students: ")
                for x in examSlot.students:
                    print(x.studentName, end=", ")
                print("\nRooms: ")
                for x in examSlot.roomsList:
                    print(x.roomNo, end=", ")
            


class Population:
    def __init__(self, size, Controller):
        self.size = size
        self.population = []    # each schedule is a chromosome

        for _ in range(size):
            self.population.append(Individual(Schedule(Controller,Controller.courseList, Controller.teacherList),Controller))

    def displayPopulation(self):
    #    for schedule in range(self.size):          # Schedules
    #        print("----------------------------------Schedule # ", schedule, "----------------------------------")
     #       self.population[schedule].displayIndividual()
       
        for i in range(self.size):
            print("Calculate fitness: ",self.population[i].calculateFitness(Controller))
       



    def selectIndividual(self,Controller): #Selects Individuals with minimum number of conflicts
        min1=float('inf')
        min2=float('inf')
        Individual1=self.population[0]
        Individual2=self.population[0]
        print("---------------------Selected Individuals--------------------------")
        for schedule in range(self.size): 
            for x in self.population:
                if (min1> x.calculateFitness(Controller)):
                #    min2=min1
                    min1=x.calculateFitness(Controller)
                    Individual1=x                                           
                elif (min2> x.calculateFitness(Controller) and x.calculateFitness(Controller)!=min1):
                    min2=x.calculateFitness(Controller)
                    Individual2=x
        
  #      Individual1.displayIndividual()
 #       Individual2.displayIndividual()
        print(Individual1.calculateFitness(Controller), Individual2.calculateFitness(Controller))
        if(Individual1.calculateFitness(Controller)==0):
            Individual1.displayIndividual()  
            sys.exit("Solution found!")
        elif (Individual2.calculateFitness(Controller)==0):
            Individual2.displayIndividual()    
            sys.exit("Solution found!")
        
   #     self.crossOver(Individual1, Individual2)
        return Individual1,Individual2
        

    def copyDay(self,offspring, individual2,dayNo): #Copies a day from parent to offspring
        offspring.daysList[dayNo].examSlotList=[]
        for i in range(len(offspring.daysList[dayNo].examSlotList)):            
            offspring.daysList[n].examSlotList[i].invigilator=[]        
            offspring.daysList[n].examSlotList[i].roomsList=[]              
           
        
        for i in range(len(individual2.daysList[dayNo].examSlotList)):            
            offspring.daysList[dayNo].examSlotList.append(individual2.daysList[dayNo].examSlotList[i])          
            offspring.daysList[dayNo].examSlotList[i].invigilator=individual2.daysList[dayNo].examSlotList[i].invigilator           
            offspring.daysList[dayNo].examSlotList[i].roomsList=individual2.daysList[dayNo].examSlotList[i].roomsList
            offspring.daysList[dayNo].examSlotList[i].course=individual2.daysList[dayNo].examSlotList[i].course

        



    def crossOver(self,Individual1,Individual2):
        #swapping alternate days in new individual
        offspring=Individual1
        i=0
        for day in offspring.chromosome.daysList:
            if (i%2==0): #taking even days from individual 1
                offspring=Individual1
            elif (i%2==1): #taking odd days from individual 2
                self.copyDay(offspring.chromosome,Individual2.chromosome, i)
            i=i+1
        print("---------------------Offspring--------------------------")
  #      offspring.displayIndividual()
        print("Offspring Fitness: ")
        print(offspring.calculateFitness(Controller))
        if(offspring.calculateFitness(Controller)==9):
            offspring.displayIndividual()
            sys.exit("Solution found!")

        return offspring,Individual1    
    #    self.mutation(offspring,Individual1)

    def mixGenes(self,offspring):
        offspringCourseList=[]
        offspringTeacherList=[]
        for days in offspring.chromosome.daysList:
            for exams in days.examSlotList:
                offspringCourseList.append(exams.course)
                for x in exams.invigilator:
                    offspringTeacherList.append(x)

        
      
        for i in range(2,self.size):
            self.population[i].chromosome=Schedule(Controller,offspringCourseList,offspringTeacherList)
                
               
             
        
       
                
     
              
        
        
        
                
        

    def mutation(self,offspring,Individual1):
        self.population[0]=offspring
        self.population[1]=Individual1

        
        print("---------------------New Generation--------------------------")
        self.mixGenes(offspring)
        
        self.displayPopulation()


        
        
        
        
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
generation=0
population = Population(20, Controller)
population.displayPopulation()



Fittest,SecondFittest=population.selectIndividual(Controller)
Offspring,Fittest=population.crossOver(Fittest,SecondFittest)
generation=generation+1

while(1):
    print("Generation# ",generation)
    NewGeneration = Population(20, Controller)
    NewGeneration.mutation(Offspring,Fittest)
    NewGeneration.displayPopulation()
    Fittest,SecondFittest=NewGeneration.selectIndividual(Controller)
    Offspring,Fittest=NewGeneration.crossOver(Fittest,SecondFittest)
    generation=generation+1
