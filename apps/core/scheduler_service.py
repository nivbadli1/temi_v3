import configparser
import utils as U
from sqlalchemy import create_engine


# Define env
config = configparser.ConfigParser()
config.read('/home/naya/TEMI_PROJECT/src/config.ini')

# Create engine
e = "mysql+pymysql://{}:{}@{}:3306/{}".format( \
    config['MYSQL']['user'], config['MYSQL']['password'], config['MYSQL']['server'], config['MYSQL']['database'])
engine = create_engine(e)

departments = U.get_all_deprtments(engine)
print(departments)
for i in departments:
    d = Deprtment(i)
    print("dept:{}".format(i))
    print(d.events)
    # d.generate_events()s