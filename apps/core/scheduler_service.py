
import utils as U

from apps.authentication.models import Users
from apps import db


# # Define env
# config = configparser.ConfigParser()
# config.read('/home/naya/TEMI_PROJECT/src/config.ini')
#
# # Create engine
# e = "mysql+pymysql://{}:{}@{}:3306/{}".format( \
#     config['MYSQL']['user'], config['MYSQL']['password'], config['MYSQL']['server'], config['MYSQL']['database'])
# engine = create_engine(e)
departments = Users.query.all()

# departments = U.get_all_deprtments(engine)
# print(departments)
for d in departments:
    d.generate_events()

    # d = Deprtment(i)
    # print("dept:{}".format(i))
    # print(d.events)
    # d.generate_events()s