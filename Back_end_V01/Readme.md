		       _ ______ ________      ________  _____ 
		      | |  ____|  ____\ \    / /  ____|/ ____|
		      | | |__  | |__   \ \  / /| |__  | (___  
		  _   | |  __| |  __|   \ \/ / |  __|  \___ \ 
		 | |__| | |____| |____   \  /  | |____ ____) |
		  \____/|______|______|   \/   |______|_____/ 
		                                              
________________________________________________________________________________________________
________________________________________________________________________________________________

Description : 
-------------

partie back en constuction fast api et unicorne


Codeur   : K.Azazel   |

Language : Python3    |

Date     : 16/11/2021 |
________________________________________________________________________________________________
________________________________________________________________________________________________

# Route en Faite :

nous avons deja plusieur route qui mene vers 

* /usr :
	*	Return un message usr

* /account_info :
	*	Return un message les information du compte:
		* login
		* balance
		* equity
		* levier
		* broker
		* server

* /ticker_live/{ticker_id} :
	* Return les Donner en live du symbole selectionner qui sont de type :
			* Ask
			* Bid
			* Med
			* Time

* /symbol_info/{item_id}:
	* Return les informations de recuperation du symbol en cours

* /all_symbol : 
	* Return Tous les symbole Tradable par le Broker 
