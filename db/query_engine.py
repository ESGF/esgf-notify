
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models.notify import ESGFSubscribers, ESGFTerms
from models.security import ESGFUser


class QueryEngine():

	def __init__(self, dburl):
		engine = create_engine(dburl, echo=False)
		self.Session = sessionmaker(bind=engine)
		self.lastid = -1

		session = self.Session()

		self.query_res = session.query(ESGFSubscribers,ESGFUser.email,ESGFTerms.keyname,ESGFTerms.valuename).join(ESGFUser).join(ESGFTerms)
		session.close()

	def get_rows():

		result_dict = {}
		last_id = -1
		email = ''
		for x in self.query_res:

			if not last_id 	== x[0].id:
				if last_id > -1
					yield (x[1], result_dict)
			last_id = x[0].id
			result_dict[x[2]] = x[3]
			email=x[1]

		yield (email, result_dict)


qe = QueryEngine('postgresql://dbsuper:esgrocks@localhost/esgcet')

for i, x in enumerate qe.get_rows():

	print i + 1, str(x)



