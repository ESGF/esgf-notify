# comment....

class ResultTracker(object):
    """docstring f ResultTrackerme"""
    def __init__(self):
        self.user_res_dict = {}

    def track_results(self, user, results):
        """  for a user and a raw set of results,  determine the update status codes,
        ie retractions, new versions, new datasets"""

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
                    tmp_i = next_i + 1

                    next_item = sorted_res[tmp_i]
                    if latest_master == next_item["master_id"]:
                        assert not next_item["latest"]
                        item["update_status"] = "new-version"
                        if not appended:
                            outres.append(item)
                            appended = True
                    else:
                        if not appended:
                            item["update_status"] = "new-dataset"
                            outres.append(item)
                            break
                    next_i += 1

        if user in self.user_res_dict:
            tmp = self.user_res_dict[user]
            tmp.append(outres)
            self.user_res_dict[user] = tmp
        else:
            self.user_res_dict[user] = [outres]

# what if the dataset was retracted then new version published?
#  Does the retracted dataset get its timestamp updated?

    def combine_user_res(self):
        """combines lists of results per-user to a single list"""
        outdict = {}
        user_res_dict = self.user_res_dict

        for user in user_res_dict:

            outdict[user] = [x for y in user_res_dict[user] for x in y]

        return outdict
