import random
import os
import platform

"""
Clases:

Jugador, Banco, Casilla, Tablero, Monopoly

"""

prompt = ["","","","","","","","","","","",""]     # Missatges del joc a mostrar al jugador

# Funció per netejar la pantalla
def clearScreen():
    sistema = platform.system()
    os.system('cls' if sistema == "Windows" else 'clear')

def promptEsborrar():
    global prompt
    prompt.clear()

def promptAfegir(text):
    global prompt
    prompt.append(text)
    if len(prompt) > 12:
        prompt.pop(0)

def promptDibuixar():
    global prompt
    for missatge in prompt:
        print(missatge)

class Banco:
    def __init__(self):
        self.dinero = 1000000

    def actualizarDinero(self):
        if self.dinero <= 500000:
            self.dinero += 1000000

        return self.dinero
    
class Jugador:
    def __init__(self, color):
        self.color = color
        self.dinero = 2000
        self.propiedades = []
        self.posicion = 0
        self.enCarcel = False
        self.turnosEnCarcel = 0
        self.cartaSalirCarcel = False

    def moverse(self, pasos):   
        self.posicion += pasos
        if self.posicion > 23:
            self.posicion = self.posicion - 24

        return self.posicion
    
    def pagar(self, cantidad):
        if cantidad <= self.dinero:
            self.dinero -= cantidad
            return True
        else: 
            promptAfegir(f"{self.color} no té suficients diners")
            return False

    def cobrar(self, cantidad):
        self.dinero += cantidad 

    def salirCarcel(self):
        if self.cartaSalirCarcel:
            self.enCarcel = False
            self.cartaSalirCarcel = False
            promptAfegir(f"{self.color} utilitza la carta per sortir")
        elif self.turnosEnCarcel >= 3:
            self.enCarcel = False
            self.turnosEnCarcel = 0
            promptAfegir(f"{self.color} has sortit de la presó")
        else:
            self.turnosEnCarcel += 1
            promptAfegir(f"{self.color} porta {self.turnosEnCarcel} a la presó")



class Casilla:
    def __init__(self, nombre, tipo, alquilerCasa, alquilerHotel, precio, precioComprarCasa, precioComprarHotel, propietario = None):
        self.nombre = nombre
        self.propietario = propietario
        self.jugadores = []
        self.tipo = tipo
        self.precio = precio
        self.alquilerCasa = alquilerCasa
        self.alquilerHotel = alquilerHotel
        self.casas = 0
        self.hoteles = 0
        self.precioComprarCasa = precioComprarCasa
        self.precioComprarHotel = precioComprarHotel

    def __repr__(self):
        return self.nombre

    def tipoCasilla(self):
        return self.tipo
    
    def comprarTerreno(self, jugador):
        terrenos = {
            "Lauria": 50, "Rosselló": 50, "Marina": 50, "C. de cent": 50,
            "Muntaner": 60, "Aribau": 60, "Sant Joan": 60, "Aragó": 60,
            "Urquinaona": 70, "Fontana": 70, "Les Rambles": 70, "Pl. Catalunya": 70,
            "P. Àngel": 80, "Via Augusta": 80, "Balmes": 80, "Pg. de Gràcia": 80
        }
        if self.propietario is None:
            if jugador.pagar(terrenos[self.nombre]):
                self.propietario = jugador
                jugador.propiedades.append(self)
                promptAfegir(f"{jugador.color} ha comprat {self.nombre}")
            else:
                promptAfegir(f"{jugador.color} no té prous diners per comprar {self.nombre}")
        else:
            promptAfegir(f"Aquest terreny ya pertany a {self.propietario.color}")

    def cobrarAlquiler(self, jugador):
        if self.propietario and self.propietario != jugador:
            jugador.pagar(self.alquiler)
            self.propietario.cobrar(self.alquiler)
            promptAfegir(f"{jugador.color} paga {self.alquiler} a {self.propietario.color} per estar {self.nombre}")

    def precioCasa(self):
        precios = {
            "Lauria": 200, "Rosselló": 225, "Marina": 250, "C. de cent": 275,
            "Muntaner": 300, "Aribau": 325, "Sant Joan": 350, "Aragó": 375,
            "Urquinaona": 400, "Fontana": 425, "Les Rambles": 450, "Pl. Catalunya": 475,
            "P. Àngel": 500, "Via Augusta": 525, "Balmes": 550, "Pg. de Gràcia": 525
        }
        precio = precios.get(self.nombre)
        if precio is None:
            print(f"La clave '{self.nombre}' no existe en el diccionario.")
        else:
            return precio
    
    def precioHotel(self):
        precios = {
            "Lauria": 250, "Rosselló": 255, "Marina": 260, "C. de cent": 265,
            "Muntaner": 270, "Aribau": 275, "Sant Joan": 280, "Aragó": 285,
            "Urquinaona": 290, "Fontana": 300, "Les Rambles": 310, "Pl. Catalunya": 320,
            "P. Àngel": 330, "Via Augusta": 340, "Balmes": 350, "Pg. de Gràcia": 360
        }
        precio = precios.get(self.nombre)
        if precio is None:
            print(f"La clave '{self.nombre}' no existe en el diccionario")
        else:
            return precio
        
    def precios(self):
        promptAfegir(f"Preu casa: {self.precioCasa()}, Preu Hotel: {self.precioHotel()}")
        
    def invertirCasa(self, jugador):
        if self.propietario == jugador and self.casas < 4:
            coste_casa = self.precioCasa()
            if jugador.pagar(coste_casa):
                self.casas += 1
                promptAfegir(f"{jugador.color} compra una casa a {self.nombre}")
        else: 
            promptAfegir(f"{jugador.color} no té aquest terreny")

    def invertirHotel(self, jugador):
        if self.propietario == jugador and self.casas >= 2 and self.hoteles < 2:
            coste_hotel = self.precioHotel()
            if jugador.pagar(coste_hotel):
                self.hoteles += 1
                self.casas -= 2 
                promptAfegir(f"{jugador.color} ha comprat un hotel a {self.nombre}")
        else: 
            promptAfegir(f"{jugador.color} no té aquest terreny")
    

    def casillaSuerte(self, jugador):
        opciones_suerte = [
            "Salir de la cárcel", 
            "Ir a prisión", 
            "Ir a la salida", 
            "Ir tres espacios atrás", 
            "Hacer reparaciones en propiedades", 
            "Eres elegido alcalde"
        ]
        
        eleccion = random.choice(opciones_suerte)
        
        if eleccion == "Salir de la cárcel":
            jugador.cartaSalirCarcel = True
            promptAfegir(f"{jugador.color} obté per sortir de la presó")
        
        elif eleccion == "Ir a prisión":
            jugador.posicion = 6  # En tu tablero, la cárcel está en la posición 6
            jugador.enCarcel = True
            jugador.turnosEnCarcel = 0
            promptAfegir(f"{jugador.color} ha estat enviat a la presó.")

        elif eleccion == "Ir a la salida":
            jugador.posicion = 0
            jugador.cobrar(200)
            promptAfegir(f"{jugador.color} torna a la casella de sortida")
        
        elif eleccion == "Ir tres espacios atrás":
            jugador.posicion -= 3
            promptAfegir(f"{jugador.color} retrocedeix tres espais.")
        
        elif eleccion == "Hacer reparaciones en propiedades":
            total_pago = 0
            for propiedad in jugador.propiedades:
                pago = 25 * propiedad.casas + 100 * propiedad.hoteles
                total_pago += pago
            jugador.pagar(total_pago)
            promptAfegir(f"{jugador.color} ha pagat {total_pago}€ per reparacions")
        
        elif eleccion == "Eres elegido alcalde":
            for otro_jugador in self.jugadores:
                if otro_jugador != jugador:
                    otro_jugador.pagar(50)
                    jugador.cobrar(50)
            promptAfegir(f"{jugador.color} ara és alcalde, tots paguen 50€")

    
    def casillaCaja(self, jugador):
        opciones_caja = [
            "Salir de la cárcel", 
            "Ir a prisión", 
            "Error de la banca a tu favor", 
            "Gastos médicos", 
            "Gastos escolares", 
            "Reparaciones en la calle", 
            "Concurso de belleza"
        ]
        
        eleccion = random.choice(opciones_caja)
        
        if eleccion == "Salir de la cárcel":
            jugador.cartaSalirCarcel = True
            promptAfegir(f"{jugador.color} obté sortir de la presó")
        
        elif eleccion == "Ir a prisión":
            jugador.posicion = 6  # La cárcel está en la posición 6
            jugador.enCarcel = True
            jugador.turnosEnCarcel = 0
            promptAfegir(f"{jugador.color} ha estat enviat a la presó")
        
        elif eleccion == "Error de la banca a tu favor":
            jugador.cobrar(150)
            promptAfegir(f"{jugador.color} +150€ per un error de la banca")
        
        elif eleccion == "Gastos médicos":
            jugador.pagar(50)
            promptAfegir(f"{jugador.color} paga 50€ per despeses")

        elif eleccion == "Gastos escolares":
            jugador.pagar(50)
            promptAfegir(f"{jugador.color} paga 50€ per despeses")
        
        elif eleccion == "Reparaciones en la calle":
            jugador.pagar(40)
            promptAfegir(f"{jugador.color} paga 40€ per reparacions")
        
        elif eleccion == "Concurso de belleza":
            jugador.cobrar(10)
            promptAfegir(f"{jugador.color} guanya 10€ per un concurs")



class Tablero:
    def __init__(self):
        self.tablero =[]
        self.construirTablero()

    def construirTablero(self):
        listaNombres = ["Lauria", "Rosselló", "Marina", "C. de cent", "Muntaner", "Aribau" , "Sant Joan", "Aragó" , "Urquinaona", "Fontana" ,"Les Rambles", "Pl. Catalunya", "P. Àngel", "Via Augusta", "Balmes", "Pg. de Gràcia"]
        listaPrecioAlquilerCasa = [10,10,15,15,20,20,25,25,30,30,35,35,40,40,50,50]
        listaPrecioAlquilerHotel = [15,15,15,20,20,20,25,25,25,30,30,30,40,40,50,50]
        listaComprarTerreno = [50,50,50,50,60,60,60,60,70,70,70,70,80,80,80,80]
        listaComprarCasa = [200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,525]
        listaComprarHotel = [250,255,260,265,270,275,280,285,290,300,310,320,330,340,350,360] 
        for x in range(len(listaNombres)):
            self.tablero.append(Casilla(listaNombres[x], "calle", listaPrecioAlquilerCasa[x], listaPrecioAlquilerHotel[x], listaComprarTerreno[x], listaComprarCasa[x], listaComprarHotel[x]))

        """self.tablero.insert(0, Casilla("Sortida", "salida", 0, 0, 0, 0, 0))
        self.tablero.insert(3, Casilla("Sort", "suerte", 0, 0, 0, 0, 0))
        self.tablero.insert(6, Casilla("Presó", "carcel", 0, 0, 0, 0, 0))
        self.tablero.insert(9, Casilla("Caixa", "caja", 0, 0, 0, 0, 0))
        self.tablero.insert(12, Casilla("Parking", "parking", 0, 0, 0, 0, 0))
        self.tablero.insert(15, Casilla("Sort", "suerte", 0, 0, 0, 0, 0))
        self.tablero.insert(18, Casilla("Anr pró", "ir carcel", 0, 0, 0, 0, 0))
        self.tablero.insert(21, Casilla("Caixa", "caja", 0, 0, 0, 0, 0))"""

        casillasEspeciales = ["Sortida","Sort", "Presó", "Caixa", "Parking", "Sort", "Anr pró", "Caixa"]
        contador = 0
        for x in range(0, 22, 3):
            self.tablero.insert(x, Casilla(casillasEspeciales[contador], casillasEspeciales[contador], 0, 0, 0, 0, None))
            contador +=1




class Monopoly:
    def __init__(self):
        self.banco = Banco()
        self.jugadores = []
        self.tablero = Tablero()
        self.turnos = 0
        self.monopoly = self.menu()
        

    def tirarDados(self):
        return random.randint(1, 6), random.randint(1, 6)

    def crearJugadores(self):
        colores = ["Groc", "Taronja", "Vermell", "Blau"]
        for x in range(4):
            self.jugadores.append(Jugador(colores[x]))

        random.shuffle(self.jugadores)
        return self.jugadores
    
    def taulellDibuixar(self):
        t = [" "] * 24

        top = ""
        bot = ""

        for x in range(12, 19):
            top += "+----" + (str(self.tablero.tablero[x].casas) + "C" if self.tablero.tablero[x].casas != 0 else "--") + (str(self.tablero.tablero[x].hoteles) + "H" if self.tablero.tablero[x].hoteles != 0 else "--")

        for x in range(6, -1, -1):
            bot += "+----" + (str(self.tablero.tablero[x].casas) + "C" if self.tablero.tablero[x].casas != 0 else "--") + (str(self.tablero.tablero[x].hoteles) + "H" if self.tablero.tablero[x].hoteles != 0 else "--")

        for jugador in self.jugadores:
            pos = jugador.posicion
            color_inicial = jugador.color
            
            if t[pos] == " ":
                t[pos] = color_inicial[0] 
            else:
                t[pos] += color_inicial[0]  
        
        print(f"""
        +--------+--------+--------+--------+--------+--------+--------+    Banca: 
        |Parking |Urqinoa |Fontana |Sort    |Rambles |Pl.Cat  |Anr pró |    Dinero: {self.banco.dinero} 
        |{t[12]:<8}|{t[13]:<8}|{t[14]:<8}|{t[15]:<8}|{t[16]:<8}|{t[17]:<8}|{t[18]:<8}|    
        {top}+    Jugador: {self.jugadores[0].color}             
        |Aragó  {(str(self.tablero.tablero[11].casas) + "C" if self.tablero.tablero[11].casas != 0 else "|").rjust(2)}                                            {(str(self.tablero.tablero[19].casas) + "C" if self.tablero.tablero[19].casas != 0 else "|").ljust(2)} Angel |    Carrers: {str(self.jugadores[0].propiedades)[1:-1]}
        |{t[11]:<8}{(str(self.tablero.tablero[11].hoteles) + "H" if self.tablero.tablero[11].hoteles != 0 else "|").rjust(1)}   {prompt[0].ljust(41)}{(str(self.tablero.tablero[19].hoteles) + "H" if self.tablero.tablero[19].hoteles != 0 else "|").ljust(1)}{t[19]:<8}|    Dinero: {self.jugadores[0].dinero}
        +--------+   {prompt[1].ljust(41)}+--------+    Especiales: {"Sortir de la presó" if (self.jugadores[0].cartaSalirCarcel) else "(res)"}
        |S.Joan {(str(self.tablero.tablero[10].casas) + "C" if self.tablero.tablero[10].casas != 0 else "|").rjust(2)}   {prompt[2].ljust(41)}{(str(self.tablero.tablero[20].casas) + "C" if self.tablero.tablero[20].casas != 0 else "|").ljust(2)}Augusta|
        |{t[10]:<8}{(str(self.tablero.tablero[10].hoteles) + "H" if self.tablero.tablero[10].hoteles != 0 else "|").rjust(1)}   {prompt[3].ljust(41)}{(str(self.tablero.tablero[20].hoteles) + "H" if self.tablero.tablero[20].hoteles != 0 else "|").ljust(1)}{t[20]:<8}|    Jugador: {self.jugadores[1].color}
        +--------+   {prompt[4].ljust(41)}+--------+    Carrers: {str(self.jugadores[1].propiedades)[1:-1]}
        |Caixa   |   {prompt[5].ljust(41)}| Caixa  |    Dinero: {self.jugadores[1].dinero}
        |{t[9]:<8}|   {prompt[6].ljust(41)}|{t[21]:<8}|    Especiales: {"Sortir de la presó" if (self.jugadores[1].cartaSalirCarcel) else "(res)"}
        +--------+   {prompt[7].ljust(41)}+--------+
        |Aribau {(str(self.tablero.tablero[8].casas) + "C" if self.tablero.tablero[8].casas != 0 else "|").rjust(2)}   {prompt[8].ljust(41)}{(str(self.tablero.tablero[22].casas) + "C" if self.tablero.tablero[22].casas != 0 else "|").ljust(2)} Balmes|    Jugador: {self.jugadores[2].color}
        |{t[8]:<8}{(str(self.tablero.tablero[8].hoteles) + "H" if self.tablero.tablero[8].hoteles != 0 else "|").rjust(1)}   {prompt[9].ljust(41)}{(str(self.tablero.tablero[22].hoteles) + "H" if self.tablero.tablero[22].hoteles != 0 else "|").ljust(1)}{t[22]:<8}|    Carrers: {str(self.jugadores[2].propiedades)[1:-1]}
        +--------+   {prompt[10].ljust(41)}+--------+    Dinero: {self.jugadores[2].dinero}   
        |Muntan {(str(self.tablero.tablero[7].casas) + "C" if self.tablero.tablero[7].casas != 0 else "|").rjust(2)}   {prompt[11].ljust(41)}{(str(self.tablero.tablero[23].casas) + "C" if self.tablero.tablero[23].casas != 0 else "|").ljust(2)} Gracia|    Especiales: {"Sortir de la presó" if (self.jugadores[2].cartaSalirCarcel) else "(res)"}
        |{t[7]:<8}{(str(self.tablero.tablero[11].hoteles) + "H" if self.tablero.tablero[11].hoteles != 0 else "|").rjust(1)}                                            {(str(self.tablero.tablero[23].hoteles) + "C" if self.tablero.tablero[23].hoteles != 0 else "|").ljust(1)}{t[23]:<8}|
        {bot}+    Jugador: {self.jugadores[3].color}
        |        |        |        |        |        |        |        |    Carrers: {str(self.jugadores[3].propiedades)[1:-1]}
        |Presó   |Consell |Marina  |Sort    |Rossell |Lauria  |Sortida |    Dinero: {self.jugadores[3].dinero}
        |{t[6]:<8}|{t[5]:<8}|{t[4]:<8}|{t[3]:<8}|{t[2]:<8}|{t[1]:<8}|{t[0]:<8}|    Especiales: {"Sortir de la presó" if (self.jugadores[3].cartaSalirCarcel) else "(res)"}
        +--------+--------+--------+--------+--------+--------+--------+
        """)


    
    def menu(self):

        self.crearJugadores()
        while True:
            for jugador in self.jugadores:
                dado1, dado2 = self.tirarDados()
                sumaDados = dado1 + dado2
                promptAfegir(f"Juga, {jugador.color} ha sortit {dado1}, {dado2}")

                if jugador.enCarcel:
                    jugador.salirCarcel()

                if jugador.enCarcel and dado1 == dado2:
                    jugador.enCarcel = False
                    promptAfegir(f"{jugador.color} ha sortit de la presó")

                if not jugador.enCarcel:
                    jugador.moverse(sumaDados)

                casilla = self.tablero.tablero[jugador.posicion]
                

                while True:
                    clearScreen()
                    self.taulellDibuixar()
                    opciones = input(f"Juga {jugador.color} opcions: passar(1), comprar terreno(2), comprar casa(3), comprar hotel(4), preus(5), precio banco(6), precio jugador(7), vender banco(8), vender jugador(9): ")
                    if opciones in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        break
                    else:
                        print("Valor no valido")
                if casilla.tipo == "calle":
                    if opciones == "1":
                        promptAfegir(f"{jugador.color} pasa torn")
                    elif opciones == "2":
                        casilla.comprarTerreno(jugador)
                    elif opciones == "3":
                        casilla.invertirCasa(jugador)
                    elif opciones == "4":
                        casilla.invertirHotel(jugador)
                    elif opciones == "5":
                        casilla.precios()
                    elif opciones == "6":
                        if casilla in jugador.propiedades:
                            numCasas = casilla.casas
                            numHoteles = casilla.hoteles
                            precioCasas = numCasas * casilla.precioCasa()
                            precioHoteles = numHoteles * casilla.precioHotel()
                            promptAfegir(f"Es poden vendre al banc per: {(precioCasas + precioHoteles) // 2}")
                        else:
                            promptAfegir("Aquesta casella no es propietat teva")
                    elif opciones == "7":
                        if casilla in jugador.propiedades:
                            numCasas = casilla.casas
                            numHoteles = casilla.hoteles
                            precioCasas = numCasas * casilla.precioCasa()
                            precioHoteles = numHoteles * casilla.precioHotel()
                            promptAfegir(f"Es poden vendre a altre jugador per: {int((precioCasas + precioHoteles) * 0.9)}")
                        else:
                            promptAfegir("Aquesta casella no es propietat teva")
                    elif opciones == "8":
                        if casilla in jugador.propiedades:
                            numCasas = casilla.casas
                            numHoteles = casilla.hoteles
                            precioCasas = numCasas * casilla.precioCasa()
                            precioHoteles = numHoteles * casilla.precioHotel()
                            precioTotal = (precioCasas + precioHoteles) // 2
                            jugador.cobrar(precioTotal)
                            casilla.casas = 0
                            casilla.hoteles = 0
                            jugador.propiedades.remove(casilla)
                            promptAfegir(f"Has venut {casilla.nombre} al banc")
                        else:
                            promptAfegir("Aquesta casella no es propietat teva")
                    elif opciones == "9":
                        if casilla in jugador.propiedades:
                            while True:
                                opcion = input("A quin jugador s'ho vols vendre (color): ")
                                if opcion in ["Vermell", "Groc", "Blau", "Taronja"]:
                                    break
                                else:
                                    print("Valor no valido")
                            numCasas = casilla.casas
                            numHoteles = casilla.hoteles
                            precioCasas = numCasas * casilla.precioCasa()
                            precioHoteles = numHoteles * casilla.precioHotel()
                            precioTotal = int((precioCasas + precioHoteles) * 0.9)
                            jugador.cobrar(precioTotal)
                            jugador.propiedades.remove(casilla)
                            for jugador2 in self.jugadores:
                                if jugador2.color == opcion:
                                    jugador2.pagar(precioTotal)
                                    jugador2.propiedades.append(casilla)
                                    casilla.propietario = jugador2
                        else:
                            promptAfegir("Aquesta casella no es propietat teva")
                elif casilla.tipo == "Sortida":
                    jugador.cobrar(200)
                elif casilla.tipo == "Sort":
                    casilla.casillaSuerte(jugador)
                elif casilla.tipo == "Caixa":
                    casilla.casillaCaja(jugador)
                elif casilla.tipo == "Parking":
                    promptAfegir(f"{jugador.color} no fa res aquest torn")
                elif casilla.tipo == "Anr pró":
                    promptAfegir(f"{jugador.color} va a la presó directament")
                    jugador.posicion = 6
                    jugador.enCarcel = True
                        

monopoly = Monopoly()

monopoly