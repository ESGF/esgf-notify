
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from db.models.notify import ESGFSubscribers, ESGFTerms
from db.models.security import ESGFUser
from

class QueryEngine():

	def __init__(self, dburl):
		engine = create_engine(dburl, echo=False)
		self.Session = sessionmaker(bind=engine)


	def get_rows(self):

		session = self.Session()

		res = session.query(Subscribers,User.email,Terms).join(User).join(Terms)


		for x in res:
			print x.email, x.keyname, x.valuename


qe = QueryEngine('postgresql://dbsuper:esgrocks@localhost/esgcet')
qe.get_rows()
