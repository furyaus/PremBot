@staticmethod
def get_key_by_value(value, dict_to_search):
    for dkey, dvalue in dict_to_search.item():
        if dvalue == value:
            return dkey
    return -1

# Team list
def updateTeamList(team_list,user_id,team_id):
    team_list.update({str(user_id): {'team': team_id}})
    return team_list