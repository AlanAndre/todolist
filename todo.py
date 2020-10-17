from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_func():
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if not rows:
        print('Nothing to do!\n')
    else:
        for i, j in enumerate(rows, start=1):
            print('{0}. {1}\n'.format(i, j))


def week_func():
    for i in range(7):
        print('\n{0}'.format((datetime.today() + timedelta(days=i)).date().strftime('%A %d %b')))
        rows = session.query(Table).filter(Table.deadline ==
                                           (datetime.today().date() + timedelta(days=i))).all()
        if not rows:
            print('Nothing to do!')
        else:
            for j in rows:
                print(j)
    print()


def all_tasks():
    print('All tasks:')
    rows = session.query(Table).all()
    if not rows:
        print('Nothing to do!\n')
    else:
        for i, j in enumerate(rows, start=1):
            print('{0}. {1}. {2}\n'.format(i, j, j.deadline.strftime('%d %b')))


def missed_tasks():
    rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < datetime.today().date()).all()
    if rows:
        for i, j in enumerate(rows, start=1):
            print('{0}. {1}. {2}'.format(i, j, j.deadline.strftime('%d %b')))
    else:
        print('Nothing is missed!')
    print()


def add_task():
    _task = input('Enter task\n')
    _deadline = input('Enter deadline\n')
    _year = int(_deadline[:4])
    _month = int(_deadline[5:7])
    _day = int(_deadline[8:])
    _deadline = datetime(_year, _month, _day).date()
    new_task = Table(task=_task, deadline=_deadline)
    print(new_task)
    session.add(new_task)
    session.commit()
    print('The task has been added!\n')


def delete_task():
    rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < datetime.today().date()).all()
    if rows:
        print('Chose the number of the task you want to delete:')
        for i, j in enumerate(rows, start=1):
            print('{0}. {1}. {2}'.format(i, j, j.deadline.strftime('%d %b')))
        num = int(input())
        specific_row = rows[num - 1]
        session.delete(specific_row)
        session.commit()
        print('The task has been deleted!\n')
    else:
        print('Nothing to delete\n')


while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    user_input = input()
    if user_input == '0':
        print('\nBye!')
        break
    elif user_input == '1':
        today_func()
    elif user_input == '2':
        week_func()
    elif user_input == '3':
        all_tasks()
    elif user_input == '4':
        missed_tasks()
    elif user_input == '5':
        add_task()
    elif user_input == '6':
        delete_task()

