import sqlite3 #For the database use
import hashlib #This library is for the encryption of the password
import getpass #This library is for getting passwords securely
from datetime import date #This library is for extracting the date


conn = sqlite3.connect('erp_db.db') #Connection to the database

#Function to convert a list of products into a dictionary so that it contains the products and the number of their occurences in that list
def listDict(panier) :
	dict_prod = {}
	for ident in panier:
	    if ident in dict_prod:
	        dict_prod[ident] += 1
	    else:
	        dict_prod[ident] = 1

	return dict_prod


#Function to check if an item exists and is in stock by its number
def itemExists(code) :
	rows = conn.execute('SELECT code_produit, stock_produit FROM Produit');
	for row in rows:
		if row[0] == code and row[1] > 0:
			return True

	return False

#Function to print all products
def returnProducts() :
	print("\n")
	rows = conn.execute('SELECT * FROM Produit');
	for row in rows:
		print("{} - {} \t (Prix : {})".format(row[0], row[1], row[2]))


#Function to print all invoices
def returnInvoices() :
	print("\n")
	rows = conn.execute("SELECT * FROM Facture");
	for row in rows:
		print("Num Facture: {} | Code Client: {} | Nom Client: {} | Total Facture: {} | Num Commande: {}".format(row[0], row[1], row[2], row[3], row[4]))

#Function to return all orders with their products
def returnOrdersProd() :
	print("\n")
	orders = conn.execute("SELECT * FROM Commande")
	for order in orders:
		print("\nNum Commande: {} | Code Client: {} | Nom Client: {} | Adresse Client: {} | Date Commande: {}".format(order[0], order[1], order[2], order[3], order[4]))
		order_prods = conn.execute("SELECT code_produit, libelle_produit, quantite_pcom, prix_produit FROM ProduitCom WHERE ProduitCom.num_com = ?", (order[0],))
		for order_prod in order_prods:
			print("   Code Produit: {} | Libelle Produit: {} | Quantité Commandée: {} | Prix Unitaire: {}".format(order_prod[0], order_prod[1], order_prod[2], order_prod[3]))

#Function to return all clients
def returnClients() :
	print("\n")
	clients = conn.execute("SELECT * FROM Client")
	for client in clients:
		print("Code Client: {} | Nom Client: {} | Tel Client: {} | Adresse Client: {} | Identifiant: {}".format(client[0], client[1], client[2], client[3], client[4]))

#Function to return all orders for a client
def returnOrdersClient(code) :
	print("\n")
	orders = conn.execute("SELECT num_com, date_com FROM Commande WHERE code_client = ?", (code,))
	facts = conn.execute("SELECT total_fact FROM Facture WHERE code_client = ?", (code,))
	for order, fact in zip(orders, facts):
		print("\nNum Commande: {} | Date Commande: {} | Total Facture: {}".format(order[0], order[1], fact[0]))
		order_prods = conn.execute("SELECT libelle_produit, quantite_pcom, prix_produit FROM ProduitCom WHERE ProduitCom.num_com = ?", (order[0],))
		for order_prod in order_prods:
			print("   Libelle Produit: {} | Quantité Commandée: {} | Prix Unitaire: {}".format(order_prod[0], order_prod[1], order_prod[2]))

#Function to insert a client
#It check if a pseudoname already exists in the db; it loops until the user inserts a valid pseudoname
def insertClient() :
	nom = str(input("Donnez votre nom complet : "))
	tel = str(input("Donnez votre numero de telephone : "))
	adr = str(input("Donnez votre adresse : "))

	flag = True
	s = 0
	while flag == True:
		identifiant = str(input("Choisissez un identifiant : "))
		mdp = hashlib.sha256(getpass.getpass(prompt="Choisissez un mot de passe : ").encode()).hexdigest()
		clients = conn.execute('SELECT * FROM Client')
		for row in clients:
			if row[4] == identifiant:
				s = s+1
				print("Ce client existe deja!")
				check = str(input("Tapez 'q' pour revenir ou autre pour reessayer : "))
				if (check.lower() == 'q') :
					mainMenu()
				else : 
					break
		if s == 0:
			flag = False


	conn.execute("INSERT INTO Client (nom_client, tel_client, adr_client, identifiant, mdp) VALUES (?, ?, ?, ?, ?)", (nom, tel, adr, identifiant, mdp))
	conn.commit()

	return identifiant

#Function to do a login
def funcLogin() :
	flag = True
	while flag == True:
		identifiant = str(input("Inserez votre identifiant : "))
		mdp = hashlib.sha256(getpass.getpass(prompt="Veuillez saisir votre mot de passe : ").encode()).hexdigest()
		clients = conn.execute('SELECT * FROM Client')
		for row in clients:
			if row[4] == identifiant and row[5] == mdp:
				print("Bienvenue!")
				flag = False
				break
		if flag == True:
			print("Identifiant et/ou mot de passe invalide(s) !")
			check = str(input("Tapez 'q' pour revenir ou autre pour reessayer : "))
			if (check.lower() == 'q') :
				mainMenu()
				break

	return identifiant


#Function to order items
#Several changes will be made to the database including : invoice creation, order creation, etc.
#To order items, the user will have to indicate the index of each item seperately
def orderItems(code) :
	cursor = conn.cursor() #This is used to recuperate the lastrowid
	today = date.today() #This is used for the date of orders
	returnProducts() #This is used to show the products so the user can order
	panier = [] #We initialise the cart
	total = 0.0 #We initialise the sum of all products ordered

	print("Tapez 'q' quand vous avez choisi tous vos produits")
	while True:
		choix = str(input("Donnez le numero du produit à ajouter au panier : "))
		if choix == 'q' :
			break
		elif itemExists(int(choix)) :
			panier.append(int(choix)) #We add the product to the cart when the user chooses it
			line = conn.execute("SELECT prix_produit, stock_produit FROM Produit WHERE code_produit = ?", (choix,))
			for p in line:
				prix = p[0]
				stock_porduit = p[1]
			total = total + prix #Here we recuperate the price so we can add it to the sum
			conn.execute("UPDATE Produit SET stock_produit = ? WHERE code_produit = ?", ((stock_porduit - 1), choix)) #We decrement the stock
			conn.commit()
			pass
		else :
			print("Le produit que vous cherchez est soit inexistant ou hors stock!")
			pass

	if len(panier) > 0 : #If the user actually chose products
		print("Vous avez choisi : {}".format(panier))
		print("Prix total : {}".format(total))
		client = conn.execute("SELECT code_client, nom_client, adr_client FROM Client WHERE Client.identifiant = ?", (code,))
		for row in client :
			code_client = row[0]
			nom_client = row[1]
			adr_client = row[2]
		#Here we recuperated information about the client so we can use it afterwards when creating the invoice, the order and the products ordered

		#Here we will create a record of the order in the Commande table
		cursor.execute("INSERT INTO Commande (code_client, nom_client, adr_client, date_com) VALUES (?, ?, ?, ?)", (code_client, nom_client, adr_client, str(today)))
		num_com = cursor.lastrowid #Here we recuperate the num_com we just inserted
		conn.commit()

		#Here we will create a record of the invoice in the Facture table
		cursor.execute("INSERT INTO Facture (code_client, nom_client, total_fact, num_com) VALUES (?, ?, ?, ?)", (code_client, nom_client, total, num_com))
		num_fact = cursor.lastrowid #Here we recuperate the num_fact we just inserted
		conn.commit()

		panier_dict = listDict(panier) #We convert the list into a dictionary so we can have the products and keys and their occurences as values
		for produit, occ in panier_dict.items() : #For each product ordered
			row = conn.execute("SELECT libelle_produit, prix_produit From Produit WHERE code_produit = ?", (produit,)) #We recuperate information about the product so we can use it
			for l in row:
				libelle_produit = l[0] #We recuperate the product name
				prix_produit = l[1] #We recuperate the price of the product
			#Here we will insert each product of the order in a single record
			conn.execute("INSERT INTO ProduitCom (num_com, code_produit, num_fact, libelle_produit, quantite_pcom, prix_produit) VALUES (?, ?, ?, ?, ?, ?)", (num_com, produit, num_fact, libelle_produit, occ, prix_produit))
			conn.commit()

	else : #If the user didn't choose products
		print("Vous n'avez choisi aucun produit !")



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

#Menu for Admin
def menuAdmin() :
	flag = True
	while flag == True:	
		identifiant = str(input("Inserez l'identifiant de l'administrateur : "))
		mdp = getpass.getpass(prompt="Veuillez saisir le mot de passe de l'administrateur : ")

		if identifiant == "admin" and mdp == "admin_erp23*" :
			while True:
				print("\nChoisissez une option :")
				print("01 - Voir toutes les factures")
				print("02 - Voir toutes les commandes")
				print("03 - Voir tous les produits")
				print("04 - Voir tous les clients")
				print("05 - Retour")
				print("99 - Quitter")

				choix = str(input("   Votre choix : "))

				if choix == '1' or choix == '01':
					returnInvoices()
					pass
				elif choix == '2' or choix == '02':
					returnOrdersProd()
					pass
				elif choix == '3' or choix == '03':
					returnProducts()
					pass
				elif choix == '4' or choix == '04':
					returnClients()
					pass
				elif choix == '5' or choix == '05':
					menuAdmin()
				elif choix == '99':
					mainMenu()
				else:
					print("Choisissez un nombre correct")
					pass
		else:
			print("Identifiant et/ou mot de passe incorrecte(s)!")
	


#Menu for Client
def menuClient() :
	flag = True
	while flag == True:	
		code = None	
		print("Choisissez :")
		print("01 - S'authentifier")
		print("02 - Creer un compte")
		choix = str(input("   Votre choix : "))

		if choix == '1' or choix == '01' or choix == '2' or choix == '02':
			flag = False
			if choix == '1' or choix == '01':
				code = funcLogin()
			if choix == '2' or choix == '02':
				code = insertClient()
		else:
			print("Veuillez saisir un nombre correct")

	codes = conn.execute("SELECT code_client FROM Client WHERE identifiant = ?", (code,))
	for code2 in codes:
		code_cl = code2[0]

	#This is the menu where the user can choose any function
	while True:
		print("\nChoisissez une option :")
		print("01 - Voir tous les produits")
		print("02 - Commander des produits")
		print("03 - Voir vos commandes")
		print("04 - Retour")
		print("99 - Quitter")

		choix = str(input("   Votre choix : "))

		if choix == '1' or choix == '01':
			returnProducts()
			pass
		elif choix == '2' or choix == '02':
			orderItems(code)
			pass
		elif choix == '3' or choix == '03':
			returnOrdersClient(code_cl)
		elif choix == '4' or choix == '04':
			menuClient()
		elif choix == "99":
			mainMenu()
		else:
			print("Choisissez un nombre correct")
			pass
	

#Main Menu
def mainMenu() :
	flag = True
	while flag == True:		
		print("\n\nChoisissez :")
		print("01 - Admin")
		print("02 - Client")
		print("99 - Quitter")
		choix = str(input("   Votre choix : "))

		if choix == '1' or choix == '01' or choix == '2' or choix == '02':
			flag = False
			if choix == '1' or choix == '01':
				menuAdmin()
			if choix == '2' or choix == '02':
				menuClient()
		elif choix == "99":
			print("\nA la prochaine!")
			exit()
		else:
			print("Veuillez saisir un nombre correct")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #

#Test
mainMenu()


conn.close()