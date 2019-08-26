

class ResultTracker(object):
 	"""docstring f ResultTrackerme"""
 	def __init__(self):
 		self.user_res_dict = {}


	def track_results(self, user, results):

		sorted_res = sorted(results, key=lambda x: (getattr(x, 'master_id'), getattr(x, 'version')))
		outres = []

		next_i = 0

		for i, item in enumerate(sorted_res):

			# skip ahead if we have compared the current item to the previous

			if item["retracted"]:

				item["update_status"] = "new-retraction"
				outres.append(item)

			# move past the items that we scanned 
			if  i < next_i:
				continue

			if item["latest"]:
				latest_master = item["master_id"]
				next_i = i
				do_loop = True
				appended = False

				while do_loop:
					tmp_i = next_i + 1:

					next_item = sorted_res[tmp_i]
					if latest_master == next_item["master_id"]:
						assert ( next_item["latest"] == False)
						item["update_status"] = "new-version"
						if not appended:
							outres.append(item)
							appended = True
					else:
						if appended = False:
							item["update_status"] = "new-dataset"
							outres.append(item)
						break
					next_i += 1 
		if user in user_res_dict:				
			tmp = user_res_dict[user]	
			tmp.append(outres)
			user_res_dict[user] = tmp
		else:
			user_res_dict[user] = [outres]

# what if the dataset was retracted then new version published?  Does the retracted dataset get its timestamp updated?


	def combine_user_res(self):

		outdict = {}
		user_res_dict = self.user_res_dict

		for user in user_res_dict:

			outdict[user_res_dict] = [x for y in user_res_dict[user] for x in y]

		return outdict



