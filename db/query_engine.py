
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models.notify import ESGFSubscribers, ESGFTerms
from models.security import ESGFUser


class QueryEngine():

	def __init__(self, dburl):
		engine = create_engine(dburl, echo=False)
		self.Session = sessionmaker(bind=engine)


	def get_rows(self):

		session = self.Session()

		res = session.query(ESGFSubscribers,ESGFUser.email,ESGFTerms.keyname,ESGFTerms.valuename).join(ESGFUser).join(ESGFTerms)


		for x in res:
			print str(x)


qe = QueryEngine('postgresql://dbsuper:esgrocks@localhost/esgcet')
qe.get_rows()
