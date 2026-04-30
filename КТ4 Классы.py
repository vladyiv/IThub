class User:

  __count = 0

  @staticmethod
  def get_count(): return User.__count

  def __init__(self, name: str, login: str, password: str, grade: int = 1):
    if grade <= 0: print('Значение grade должно быть положительным! Присвоено значение по умолчанию.')
    self.name = name
    self.__login = login
    self.password = password
    self.grade = grade
    User.__count += 1
  
  def show_info(self):
    role_name = ''
    if type(self) == SuperUser: role_name = f', Role: {self.role}' 
    print(f'Name: {self.name}, login: {self.__login}' + role_name)

  def __lt__(self, user: 'User'): return self.grade < user.grade

  def __gt__(self, user: 'User'): return self.grade > user.grade

  def __eq__(self, user: 'User'): return self.grade == user.grade

  @property
  def grade(self): return 'Неизвестное свойство grade'
  @grade.setter
  def grade(self, value): print('Неизвестное свойство grade')

  @property
  def password(self): return '*' * len(self.__password)
  @password.setter
  def password(self, value):        
      self.__password = value

  @property
  def login(self): return self.__login
  @login.setter
  def login(self, value): print('Невозможно изменить логин!')


class SuperUser(User):

  __count = 0

  @staticmethod
  def get_count(): return SuperUser.__count

  def __init__(self, name: str, login: str, password: str, role: str, grade: int):
    super().__init__(name, login, password, grade)
    self.role = role
    SuperUser.__count += 1

  def show_info(self):
    super().show_info()