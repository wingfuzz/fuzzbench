from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import DATABASE_NAME

Base = declarative_base()


class CoverageData(Base):
    __tablename__ = 'coverage_data' 

    id = Column(Integer, primary_key=True)
    coverage = Column(Float)
    cover_pc = Column(Integer)
    total_pc = Column(Integer)
    fuzzer_id = Column(Integer, ForeignKey('fuzzers.id'))
    fuzzer = relationship("Fuzzers", back_populates="coverages")

    def __str__(self):
        return f"id: {self.id}, coverage: {self.coverage}"
    
    def __repr__(self):
        return self.__str__()


class CrashesData(Base):
    __tablename__ = 'crashes_data'

    id = Column(Integer, primary_key=True)
    crashe_case = Column(String(256))
    fuzzer_id = Column(Integer, ForeignKey('fuzzers.id'))
    fuzzer = relationship("Fuzzers", back_populates="crashes")

    def __str__(self):
        return f"id: {self.id}, crashe_case: {self.crashe_case}"
    
    def __repr__(self):
        return self.__str__()
    

class Fuzzers(Base):
    __tablename__ = 'fuzzers'
    id = Column(Integer, primary_key=True)
    fuzzer_name = Column(String(50))
    coverages = relationship("CoverageData", order_by=CoverageData.id, back_populates='fuzzer')
    crashes = relationship("CrashesData", order_by=CrashesData.id, back_populates='fuzzer')

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Projects", back_populates="fuzzers")

    def __str__(self):
        return f"id: {self.id}, fuzzer_name: {self.fuzzer_name}, coverage: {self.coverages}, crashe: {self.crashes}"
    
    def __repr__(self):
        return self.__str__()
    

class Projects(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    project_name = Column(String(50))
    fuzzers = relationship("Fuzzers", order_by=Fuzzers.id, back_populates="project")

    benchmark_id = Column(Integer, ForeignKey('benchmarks.id'))
    benchmark = relationship("Benchmarks", back_populates="projects")
    
    def __str__(self):
        return f"id: {self.id}, project_name: {self.project_name}, fuzzers: {self.fuzzers}"

    def __repr__(self):
        return self.__str__()
    

class Benchmarks(Base):
    __tablename__ = 'benchmarks'
    
    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)
    projects = relationship("Projects", order_by=Projects.id, back_populates="benchmark")
    
    def __str__(self):
        return f"id: {self.id}, start: {self.start}, end: {self.end}"

    def __repr__(self):
        return self.__str__()
    

if __name__ == "__main__":
    engine = create_engine(DATABASE_NAME, echo=True)
    Base.metadata.create_all(engine)

