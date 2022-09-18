

Session = sessionmaker(bind=engine)
session = Session()

d = Deprtment(1)
# print(departments)

d.generate_events()
