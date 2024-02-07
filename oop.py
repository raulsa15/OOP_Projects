#Class and Instances
import datetime

class Employee:
    
    #Class Variables
    raise_amount=1.04
    num_emp=0
    
    def __init__(self, first, last, pay):
        
        self.first=first
        self.last=last
        self.pay=pay
        # self.email=first+'.'+last+'@augme.com.br'
        
        Employee.num_emp+=1
    
    #method fullname
    #input a property decorator (so we can use it as class but still a method), so everytime we change the part of a name the email will be afected
    @property   #this is a property of the class
    def email(self):
        return self.first + '.' + self.last+'@augme.com.br'
    
    @property
    def fullname(self):
        return self.first + ' ' + self.last
    
    @fullname.setter
    def fullname(self, name):
        first, last=name.split(' ')
        self.first=first
        self.last=last
        
    # @fullname.deleter
    # def fullname(self, name):
    #     self.first=None
    #     self.last=None
    
    def apply_raise(self):
        self.pay=int(self.pay*self.raise_amount)
    
    #Special method to debug (visual of object) ->> minimum
    def __repr__(self):
        return "Employee('{}','{}'.'{}')".format(self.first, self.last, self.pay)
    
    #Special method to show readable version of objetc: there're plenty of special methods we can use or create in our classes
    def __str__(self):
        return '{} - {}'.format(self.fullname(), self.email)
    
    #Dunder add method
    def __add__(self, other):
        return self.pay + other.pay
        
    @classmethod #study about decorators (receive class as first argument instead of instance)
    def set_raise(cls, amount):
        cls.raise_amount=amount
        
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay= emp_str.split('-')
        return cls(first, last, pay)        
                
    @staticmethod
    def is_workday(day):
        if day.weekday()==5 or day.weekday==6:
            return False
        else:
            return True

#Inheritance: creating subclasses

class Developer(Employee):
    
    raise_amount=1.10
    
    def __init__(self, first, last, pay, prog_lang):
        
        super().__init__(first, last, pay)
        self.prog_lang=prog_lang
        # Employee.__init__(self, first, last, pay) #idem above
        

class Manager(Employee):
    
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees=[]
        else:
            self.employees=employees
            
    def add_employee(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
            
    def remove_employee(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
            
    def print_employees(self):
        x=1
        for emp in self.employees:
            print(x,' ',emp.fullname())
            x+=1

# Special (Magic/Dunder) Methods

employee1=Developer('Raul', 'Aguiar', 50000, 'Python')

print(employee1) #how can we adjust a special method to print better than a vague object
    
#print using special methods
repr(employee1)
str(employee1)

chefe1=Manager('Heitor','Lira',500000, employees=[employee1])

employee2=Developer('Joao', 'Aguiar', 60000, 'Java')

#It only works because of dunder method add which we added 
print(employee1+employee2)

chefe1.print_employees()

chefe1.add_employee(employee2)

chefe1.print_employees()

print(chefe1.employees[0].prog_lang)

chefe1.remove_employee(employee1)

chefe1.print_employees()

print(isinstance(chefe1, Employee)) #true
print(isinstance(chefe1, Developer)) #false

print(issubclass(Developer, Employee)) #true
print(issubclass(Manager, Developer)) #false
   
#it looks for methods in order of priority Developer > Employee
print(help(Manager))

Employee.fullname(employee1)

employee1.fullname()

print(employee1.prog_lang)

employee1.apply_raise()

print(employee1.pay)

print(employee1.__dict__)

employee1.raise_amount=1.05

employee1.apply_raise()

print(employee1.pay)

print(Employee.num_emp)

Employee.set_raise(1.06)

#Now we can alter raise amount value with the class method and not only do changes for a specific object
print(Employee.raise_amount)

#Classmethods and staticmethods:

emp_str1='Joao-Aguiar-150000'
employee2=Employee.from_string(emp_str1)
print(employee2)

#Static method:

my_date=datetime.date(2024,1,18)
print(Employee.is_workday(my_date))