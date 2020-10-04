from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String
from datetime import datetime
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
    new_row = Table(task=task_to_add)
    session.add(new_row)
    session.commit()
    print("\nThe task has been added!\n")


def show_tasks():
    if session.query(Table).first():
        print("Today:")
        for ids, tasks in session.query(Table.id, Table.task).all():
            print(f"{ids}. {tasks}")
        print()
    else:
        print("\nToday:\n Nothing to do!\n")


def menu():
    menu_string = ("1) Today's tasks\n"
                   "2) Add task\n"
                   "0) Exit\n")
    while True:
        choice = int(input(menu_string))
        if choice == 1:
            show_tasks()
        elif choice == 2:
            add_task()
        elif choice == 0:
            print("Bye!")
            break


if __name__ == "__main__":
    menu()
