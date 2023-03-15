from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Date, Integer, String, ForeignKey
from config import DATABASE_NAME
from create_data_table import * 
from sqlalchemy.orm import sessionmaker
# 连接数据库
engine = create_engine(DATABASE_NAME, echo=True)

Session = sessionmaker(bind=engine)
session = Session()



# f1= Fuzzers(fuzzer_name='afl')
# f2 = Fuzzers(fuzzer_name='afl++')
# f3 = Fuzzers(fuzzer_name='coverage')

# p = Projects(project_name='bloaty_fuzz_target', fuzzers=[f1, f2, f3])

# session.add(p)

# session.commit()

ps = session.query(Projects).filter(Projects.project_name == 'bloaty_fuzz_target').all()
print(ps)
for p in ps:
    print(p)
    print(type(p))
# for p in ps:
#     print(p.fuzzers)
#     for f in p.fuzzers:
#         print(f.fuzzer_name)

