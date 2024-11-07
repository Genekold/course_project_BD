import os
from config import config
from src.dbmanager import DBManager

from dotenv import load_dotenv
from src.utils import get_employer_data, create_database, save_data_to_database

load_dotenv()
list_id_emp = os.getenv('LIST_ID_EMP')

def main():
    employer_ids = list_id_emp
    params = config()

    # data = get_employer_data(employer_ids)
    # create_database('course_project_db', params)
    # save_data_to_database(data, 'course_project_db', params)

    emp = DBManager('course_project_db', params)
    print(emp.get_vacancies_with_keyword('менеджер'))



if __name__ == '__main__':
    main()