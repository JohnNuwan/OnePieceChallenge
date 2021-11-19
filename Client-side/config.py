"""
-----------------------
Codeur   : K.Azazel   |
Language : Python3    |
Date     : 16/11/2021 |

                                              
"""

# Token Pour Communication APP
WEBHOOK_PASSPHRASE = 'UTPZJP77Ry45MTBlRUpezAmLD-OM2Lq6MNcTTSRsK1E='

"""
Partie Discord:
	# Lien Webhook Discord Scalp
	# Lien Webhook Discord Intraday
	# Lien Webhook Discord Swing
"""
# Lien Webhook Discord Scalp
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/910084409506537482/gDo7iinNt7DCcE8c9JNvJTmKQLQyeQNwBk4W-eHqzfpQl462ZCOKfkHyfknbXpWQBTSD"


"""
Partie Telegram:
	# Lien Signal Public
"""
# Telegram
TOKEN = "1801058128:AAETqJbJMjVUt6ewpjYL2ZVIU8wzIlrzJL4"
CHAT_ID = "@GOLD_SIGNAL_TESTE"


from sqlalchemy import create_engine

# Create a database connection
db_password = 'Kumara-42/600'  # Set to your own password
db_port = 6543
engine = create_engine('postgresql://postgres:{}@localhost:{}/Finance'.format(db_password, db_port))
