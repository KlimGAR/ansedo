
# con = sqlite3.connect("data.sqlite")
# cur = con.cursor()
# result = cur.execute(
#     f"""INSERT INTO profile(game, name, st, hours, description)
#     VALUES({data['game']}, {data['name']},{data['coop']}, {data['hours']}, {data['desc']})""").fetchall()
# con.close()
# # вывод данных из бд!
# con = sqlite3.connect("data.sqlite")
# cur = con.cursor()
# result_0 = cur.execute(
#     f"""SELECT game, name, st, hours, description, user_id FROM profile""").fetchall()
# con.close()