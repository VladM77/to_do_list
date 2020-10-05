from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String())
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    task_to_add = input("Enter task\n")
    task_deadline_str = input("Enter deadline\n")
    task_deadline_obj = datetime.strptime(task_deadline_str, '%Y-%m-%d')
    new_row = Table(task=task_to_add, deadline=datetime(task_deadline_obj.year,
                                                        task_deadline_obj.month, task_deadline_obj.day))
    session.add(new_row)
    session.commit()
    print("\nThe task has been added!\n")


def show_tasks_today():
    print("Today {} {}:".format(int(datetime.today().day), datetime.today().strftime("%b")))
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
    if rows:
        for ids, tasks in enumerate(rows):
            print("{}. {}".format(ids + 1, tasks))
        print("")
    else:
        print("Nothing to do!\n")


def show_tasks_week():
    rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline >= datetime.today().date(),
                                                                Table.deadline <= datetime.today() + timedelta(days=6)).all()
    # if rows:
    start_date = datetime.today().date()
    end_date = datetime.today().date() + timedelta(days=6)
    delta = timedelta(days=1)
    while start_date <= end_date:
        print("\n{} {} {}:".format(start_date.strftime('%A'), int(start_date.day), start_date.strftime('%b')))
        counter = 0
        for tasks in rows:
            if tasks.deadline == start_date:
                counter += 1
                print("{}. {}".format(counter, tasks))
        if counter == 0:
            print("Nothing to do!\n")
        start_date += delta
    # else:
    #     print("Nothing to do!\n")


def show_tasks_all():
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        for ids, tasks in enumerate(rows):
            print("{}. {}. {} {}".format(ids + 1, tasks, tasks.deadline.day,
                                         tasks.deadline.strftime('%b')))
        print("")
    else:
        print("Nothing to do!\n")


def show_missed():
    rows = session.query(Table).order_by(Table.deadline).filter(Table.deadline < datetime.today().date()).all()
    print("Missed tasks:")
    if rows:
        for ids, tasks in enumerate(rows):
            print("{}. {}. {} {}".format(ids + 1, tasks, tasks.deadline.day,
                                         tasks.deadline.strftime('%b')))
        print("")
    else:
        print("Nothing to do!\n")


def delete_task():
    print("Choose the number of the task you want to delete:")

    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        for ids, tasks in enumerate(rows):
            print("{}. {}. {} {}".format(ids + 1, tasks, tasks.deadline.day,
                                         tasks.deadline.strftime('%b')))
        print("")
        to_delete = rows[int(input()) - 1]
        session.delete(to_delete)
        session.commit()
        print("The task has been deleted!")


    else:
        print("Nothing to do!\n")

def menu():
    menu_string = ("\n1) Today's tasks\n"
                   "2) Week's tasks\n"
                   "3) All tasks\n"
                   "4) Missed tasks\n"
                   "5) Add task\n"
                   "6) Delete task\n"                  
                   "0) Exit\n")
    while True:
        choice = int(input(menu_string))
        if choice == 1:
            show_tasks_today()
        elif choice == 2:
            show_tasks_week()
        elif choice == 3:
            show_tasks_all()
        elif choice == 4:
            show_missed()
        elif choice == 5:
            add_task()
        elif choice == 6:
            delete_task()
        elif choice == 0:
            print("Bye!")
            break


if __name__ == "__main__":
    menu()
